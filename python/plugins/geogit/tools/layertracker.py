import os
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtCore, QtGui
from geogit.gui.dialogs.commitdialog import CommitDialog
from shapely.wkt import loads
from geogit import config
from geogit.gui.pyqtconnectordecorator import createRepository
from geogit.gui.dialogs.importexportdialog import ImportExportDialog
import logging
from geogitpy import geogit
from layertracking import getTrackingInfo, isTracked
from shapely.geometry.polygon import Polygon
from shapely.geometry.linestring import LineString
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.multipoint import MultiPoint
import traceback
from geogit.gui.dialogs.userconfigdialog import UserConfigDialog
from geogitpy.geogitexception import UnconfiguredUserException, GeoGitException
from geogit.gui.dialogs.smartupdatefailmessage import SmartUpdateFailMessage
               
  
_logger = logging.getLogger("geogitpy")


class LayerTracker(object):
    
    def __init__(self):
        self.featuresToUpdate = {}
        self.featuresToRemove = {}
        self.canUseSmartUpdate =  {}
        self.hasChanges = {}
    
    def trackLayer(self, layer):
        def featureDeleted(fid):            
            self.featureDeleted(layer, fid)
        layer.featureDeleted.connect(featureDeleted)
        def featuresAdded(layername, features):
            self.featuresAdded(layer, features)        
        layer.committedFeaturesAdded.connect(featuresAdded)
        def geomChanged(fid, geom):
            self.featureChanged(layer, fid)
        QtCore.QObject.connect(layer, QtCore.SIGNAL("geometryChanged(QgsFeatureId, QgsGeometry&)"), geomChanged)
        def attributeValueChanged(fid, idx, value):
            self.featureChanged(layer, fid)                                
        layer.attributeValueChanged.connect(attributeValueChanged)
        def featureTypeChanged():
            self.canUseSmartUpdate[layer.id()] = False
        layer.attributeAdded.connect(featureTypeChanged)
        layer.attributeDeleted.connect(featureTypeChanged)
        layer.editingStarted.connect(lambda: self.editingStarted(layer))
        layer.editingStopped.connect(lambda: self.editingStopped(layer))
        
    def featureChanged(self, layer, fid):
        if isTracked(layer):
            self.hasChanges[layer.id()] = True
            self.featuresToUpdate[layer.id()].add(fid) 
        
    def editingStarted(self, layer):                       
        self.featuresToUpdate[layer.id()] = set()
        self.featuresToRemove[layer.id()] = []
        self.canUseSmartUpdate[layer.id()] = True
        self.hasChanges[layer.id()] = False
    
    def featuresAdded(self, layer, features):
        if not isTracked(layer):
            return        
        for feature in features:                        
            self.hasChanges[layer.id()] = True                             
            self.featuresToUpdate[layer.id()].add(feature.id())                                    
                        
    def featureDeleted(self, layer, fid):
        if not isTracked(layer):
            return                
        if not self.canUseSmartUpdate[layer.id()]:            
            return                  
        if fid >= 0:
            self.hasChanges[layer.id()] = True                                
            fIterator = layer.dataProvider().getFeatures(QgsFeatureRequest(fid));            
            try:
                geogitfid = self._getFid(fIterator.next())
                self.featuresToRemove[layer.id()].append(geogitfid)
            except Exception, e:
                _logger.error(str(e))
                _logger.debug("No fid found in feature in layer %s. Disabing smart update" %(layer.source()))
                self.canUseSmartUpdate[layer.id()] = False
                return
    
    def editingStopped(self, layer):
        if not isTracked(layer):
            return         
        if not self.hasChanges[layer.id()]:
            return
        self.hasChanges[layer.id()] = False
        url, dest = getTrackingInfo(layer)                                 
        repo = createRepository(url, False)  
        QtGui.QApplication.restoreOverrideCursor()
        autoUpdate = config.getConfigValue(config.GENERAL, config.AUTO_UPDATE)     
        if not autoUpdate:
            ret = QtGui.QMessageBox.information(config.iface.mainWindow(), "GeoGit",
                                "You have modified a layer that was imported into the" 
                                +"following GeoGit repository:\n%s\n" % url                                
                                + "Do you want to update the repository with these changes?",
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                QtGui.QMessageBox.Yes)
            update = ret == QtGui.QMessageBox.Yes
        else:
            update = True 
        if not update:
            return  
        if self.canUseSmartUpdate[layer.id()]:
            try:
                _logger.debug("Trying smart update on layer %s and repo %s" %(layer.source(), url))
                self.doSmartUpdate(layer, dest, repo)
            except Exception, e:                     
                _logger.error(traceback.format_exc())
                _logger.debug("Smart update failed. Using import update instead")  
                if config.getConfigValue(config.GENERAL, config.SHOW_MESSAGE_ON_SMART_UPDATE_FAIL):
                    dlg = SmartUpdateFailMessage(config.iface.mainWindow(), e.args[0])
                    dlg.exec_()               
                self.doUpdateLayer(layer, dest, repo)                                     
        else:
            self.doUpdateLayer(layer, dest, repo)  
        del self.featuresToUpdate[layer.id()]
        del self.featuresToRemove[layer.id()]
        del self.canUseSmartUpdate[layer.id()]
        del self.hasChanges[layer.id()]
        unstaged = repo.difftreestats(geogit.HEAD, geogit.WORK_HEAD)
        total = 0
        for counts in unstaged.values():                                
            total += sum(counts)   
        if total == 0:
            return                 
        dlg = CommitDialog(repo, config.iface.mainWindow())
        dlg.exec_()
        explorer = config.explorer 
        if dlg.getPaths() is not None:            
            repo.add(dlg.getPaths())
            try:
                repo.commit(dlg.getMessage())
            except UnconfiguredUserException, e:
                configdlg = UserConfigDialog(config.iface.mainWindow())
                configdlg.exec_()
                if configdlg.user is not None:
                    repo.config(geogit.USER_NAME, configdlg.user)
                    repo.config(geogit.USER_EMAIL, configdlg.email)
                    repo.commit(dlg.getMessage())
                else:
                    return                                        
            if (explorer is not None and explorer.currentRepo is not None 
                    and explorer.currentRepo.url == url):                
                explorer.updateRepoStatusLabelAndToolbar()                
                explorer.updateCommitsList()
            config.iface.messageBar().pushMessage("Repository correctly updated", 
                                                      level=QgsMessageBar.INFO, duration = 4)
        else:
            if (explorer is not None and explorer.currentRepo is not None 
                    and explorer.currentRepo.url == url):
                explorer.updateRepoStatusLabelAndToolbar()                
            config.iface.messageBar().pushMessage("Changes imported but not commited", 
                                                      level=QgsMessageBar.INFO, duration = 4)
        
    def _getFid(self, feature):
        for field in feature.fields().toList():
            if field.name().lower() == "id" or field.name().lower() == "fid":                                             
                return  feature[field.name()]        
        raise Exception("No ID field found in layer")             
        
    
    def doSmartUpdate(self, layer, dest, repo):  
        features = {}  
        geomType = None   
        geomField = "geom"
        #we try to have the same geom type as the default featuretype of the destination tree
        try:                
            ftype = repo.featuretype(geogit.HEAD, dest)                                   
            for fieldName, fieldType in ftype.iteritems():
                if fieldType in geogit.GEOMTYPES:
                    geomType = fieldType
                    geomField = fieldName
                    break             
        except GeoGitException, e:
            pass    
        for fid in self.featuresToUpdate[layer.id()]:
            fIterator = layer.getFeatures(QgsFeatureRequest(fid));            
            feature = fIterator.next()
            geom = feature.geometry()               
            wkt = geom.exportToWkt()
            shapelyGeom = loads(wkt)             
            if isinstance(shapelyGeom, Polygon) and geomType == geogit.TYPE_MULTIPOLYGON:
                shapelyGeom = MultiPolygon([shapelyGeom])
            elif isinstance(shapelyGeom, LineString) and geomType == geogit.TYPE_MULTILINESTRING:
                shapelyGeom = MultiLineString([shapelyGeom])
            elif isinstance(shapelyGeom, Polygon) and geomType == geogit.TYPE_MULTIPOINT:
                shapelyGeom = MultiPoint([shapelyGeom])  
            geogitfid = unicode(self._getFid(feature))
            geogitfid = dest + "/" + geogitfid
            attrValues = [f if not isinstance(f, QtCore.QPyNullVariant) else None for f in feature.attributes() ]
            attributes = dict(zip([f.name() for f in feature.fields()], attrValues)) 
            attributes[geomField] = shapelyGeom                                                      
            features[geogitfid] = attributes            
        if features:            
            repo.insertfeatures(features)
               
        toRemove = [dest + "/" + unicode(fid) for fid in self.featuresToRemove[layer.id()]]
        if toRemove:
            repo.removefeatures(toRemove)
            

    def doUpdateLayer(self, layer, dest, repo):            
        url, dest = getTrackingInfo(layer)  
        repo = createRepository(url, False)
        dlg = ImportExportDialog(config.iface.mainWindow(), repo, ImportExportDialog.IMPORT, 
                                 layer = layer, dest = dest, closeAfterOperation = True)            
        dlg.exec_()
