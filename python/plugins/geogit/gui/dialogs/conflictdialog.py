import os
import logging
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from geogit.ui.conflictdialog import Ui_ConflictDialog
from geogitpy.geogitexception import GeoGitConflictException
from geogitpy import geogit
from shapely.geometry.base import BaseGeometry

BASEMAP_NONE = 0
BASEMAP_OSM = 1
BASEMAP_GOOGLE = 2

resourcesPath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "resources")        
ptOursStyle = os.path.join(resourcesPath, "pt_ours.qml")
ptTheirsStyle = os.path.join(resourcesPath, "pt_theirs.qml")
lineOursStyle = os.path.join(resourcesPath, "line_ours.qml")
lineTheirsStyle = os.path.join(resourcesPath, "line_theirs.qml")
polygonOursStyle = os.path.join(resourcesPath, "polygon_ours.qml")
polygonTheirsStyle = os.path.join(resourcesPath, "polygon_theirs.qml")

layerIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "layer_group.gif"))
featureIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "geometry.png"))

_logger = logging.getLogger("geogitpy")

class ConflictDialog(QtGui.QDialog):
    
    def __init__(self, parent, repo):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.solved = False
        self.repo = repo                
        self.ui = Ui_ConflictDialog()
        self.ui.setupUi(self)
        
        self.setWindowFlags(self.windowFlags() |
                              QtCore.Qt.WindowSystemMenuHint |
                              QtCore.Qt.WindowMinMaxButtonsHint)
                
        self.ui.buttonBox.rejected.connect(self.closePressed)
        self.ui.zoomButton.clicked.connect(self.zoomPressed)
        self.ui.solveButton.clicked.connect(self.solve)
        self.ui.conflictsTree.itemClicked.connect(self.treeItemClicked) 
        self.ui.attributesTable.cellClicked.connect(self.cellClicked)
        self.ui.solveAllOursButton.clicked.connect(self.solveOurs)
        self.ui.solveAllTheirsButton.clicked.connect(self.solveTheirs)
        self.ui.baseMapCombo.currentIndexChanged.connect(self.baseMapChanged)
        
        def refreshMap():            
            self.showGeoms()
        self.ui.showTheirsCheck.stateChanged.connect(refreshMap)        
        self.ui.showOursCheck.stateChanged.connect(refreshMap)
        
        self.lastSelectedItem = None
        self.currentPath = None
        self.theirsLayer = None        
        self.oursLayer = None
        self.baseLayer = None
        
        settings = QtCore.QSettings()
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(0)
        horizontalLayout.setMargin(0)   
        self.mapCanvas = QgsMapCanvas()        
        self.mapCanvas.setCanvasColor(QtCore.Qt.white)    
        self.mapCanvas.enableAntiAliasing(settings.value( "/qgis/enable_anti_aliasing", False, type=bool))
        self.mapCanvas.useImageToRender(settings.value( "/qgis/use_qimage_to_render", False, type=bool))
        self.mapCanvas.mapRenderer().setProjectionsEnabled(True)
        action = settings.value("/qgis/wheel_action", 0, type=float)
        zoomFactor = settings.value("/qgis/zoom_factor", 2, type=float)        
        self.mapCanvas.setWheelAction(QgsMapCanvas.WheelAction(action), zoomFactor)
        horizontalLayout.addWidget(self.mapCanvas)
        self.ui.canvasWidget.setLayout(horizontalLayout)
        self.panTool = QgsMapToolPan(self.mapCanvas)   
        self.mapCanvas.setMapTool(self.panTool)      
        
        self.fillConflictsTree()  

    def fillConflictsTree(self):
        conflicts = self.repo.conflicts()
        self.paths = {}
        for path, c in conflicts.iteritems():            
            tree = os.path.dirname(path)
            if tree not in self.paths:
                item = QtGui.QTreeWidgetItem([tree])
                item.setIcon(0, layerIcon)
                self.ui.conflictsTree.addTopLevelItem(item)
                self.paths[tree] = item            
            conflictItem = ConflictItem(path, c)
            self.paths[tree].addChild(conflictItem)
            
    def cellClicked(self, row, col):
        if col > 1:
            return
        value = self.ui.attributesTable.item(row, col).value 
        self.ui.attributesTable.setItem(row, 3, ValueItem(value)); 
        self.ui.attributesTable.item(row, 0).setBackgroundColor(QtCore.Qt.white);
        self.ui.attributesTable.item(row, 1).setBackgroundColor(QtCore.Qt.white);
        self.ui.attributesTable.item(row, 3).setBackgroundColor(QtCore.Qt.white);
        attrib = self.ui.attributesTable.item(row, 2).text()        
        if attrib in self.conflicted:
            self.conflicted.remove(attrib)        
        self.updateSolveButton()
        
    def baseMapChanged(self, idx):
        if idx == BASEMAP_OSM:
            baseLayerFile = os.path.join(os.path.dirname(__file__), 
                                         os.pardir, os.pardir, "resources", "osm.xml")
        elif idx == BASEMAP_GOOGLE:
            baseLayerFile = os.path.join(os.path.dirname(__file__), 
                                         os.pardir, os.pardir, "resources", "gmaps.xml")
        else:
            self.baseLayer = None
            self.showGeoms()
            return
    
        if self.baseLayer is not None:
            QgsMapLayerRegistry.instance().removeMapLayer(self.baseLayer.id()) 
            self.baseLayer = None
        baseLayer = QgsRasterLayer(baseLayerFile, "base", "gdal")
        if baseLayer.isValid():
            self.baseLayer = baseLayer
            QgsMapLayerRegistry.instance().addMapLayer(self.baseLayer, False)
        else:
            _logger.debug("Could not load base layer") 
            
        self.showGeoms()           
    
    def treeItemClicked(self):                          
        item = self.ui.conflictsTree.selectedItems()[0]
        if self.lastSelectedItem == item:
            return
        self.lastSelectedItem = item
        if isinstance(item, ConflictItem):
            self.currentPath = item.path
            self.updateCurrentPath(item.versions)             
        
    def updateCurrentPath(self, versions):
        self.cleanCanvas()
        geoms = self.showFeatureAttributes(versions)
        self.createLayers(*geoms)
        self.showGeoms()
        
        layers = self.mapCanvas.layers()
        if layers:
            self.mapCanvas.setExtent(layers[0].extent())
            self.mapCanvas.refresh()

    def zoomPressed(self):
        layers = [lay.extent() for lay in self.mapCanvas.layers() if lay.type() == lay.VectorLayer]         
        if layers:            
            ext = layers[0]            
            for layer in  layers[1:]:                
                ext.combineExtentWith(layer)            
            self.mapCanvas.setExtent(ext)
            self.mapCanvas.refresh()
    
    def cleanCanvas(self):              
        self.mapCanvas.setLayerSet([])        
        layers = [self.oursLayer, self.theirsLayer, self.baseLayer]
        for layer in layers:
            if layer is not None:
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id()) 
        self.oursLayer = None
        self.theirsLayer = None
        self.baseLayer = None            
        
    
    def solveTheirs(self):
        ret = QtGui.QMessageBox.warning(self, "Solve conflict",
                                "Are you sure you want to solve all conflict using the 'Their' version?",
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                QtGui.QMessageBox.Yes);
        if ret == QtGui.QMessageBox.Yes:
            self.repo.solveconflicts(self.repo.conflicts().keys(), geogit.THEIRS)
            self.solved = True
            self.close()
   
    def solveOurs(self):
        ret = QtGui.QMessageBox.warning(self, "Solve conflict",
            "Are you sure you want to solve all conflict using the 'Mine' version?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.Yes);
        if ret == QtGui.QMessageBox.Yes:
            self.repo.solveconflicts(self.repo.conflicts().keys(), geogit.OURS)
            self.solved = True
            self.close()     
                          
    def solve(self):       
        attribs = {}
        for i in xrange(self.ui.attributesTable.rowCount()):
            value = self.ui.attributesTable.item(i, 3).value
            name = unicode(self.ui.attributesTable.item(i, 2).text())            
            attribs[name] = value            
        self.repo.solveconflict(self.currentPath, attribs)        
        parent = self.lastSelectedItem.parent() 
        parent.removeChild(self.lastSelectedItem)
        if parent.childCount() == 0:
            self.ui.conflictsTree.invisibleRootItem().removeChild(parent)
        self.lastSelectedItem = None
        self.ui.attributesTable.setRowCount(0) 
        self.cleanCanvas()
        self.ui.solveButton.setEnabled(False)
        self.solved = True
        
    def updateSolveButton(self):
        self.ui.solveButton.setEnabled(len(self.conflicted) == 0)
    
    def showFeatureAttributes(self, versions):            
        oursgeom = None
        theirsgeom = None
        self.conflicted = []
        allAttribs = set()
        for v in versions:
            for a in v.attributes:
                allAttribs.add(a)                        

        self.ui.attributesTable.setRowCount(len(allAttribs))        
        
        for idx, name in enumerate(allAttribs):
            values = [v.attributes.get(name, None) for v in versions]
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item = QtGui.QTableWidgetItem(name)
            item.setFont(font)            
            self.ui.attributesTable.setItem(idx, 2, item);
            for i, v in enumerate(values[1:]):            
                self.ui.attributesTable.setItem(idx, i, ValueItem(v));                                    
            
            self.ui.attributesTable.setItem(idx, 3, ValueItem(None)); 
            
            def _equal(a, b):     
                if isinstance(a, BaseGeometry) and isinstance(b, BaseGeometry):                    
                    return a.to_wkt() == b.to_wkt()                    
                else:
                    return a == b
                                    
            ok =  _equal(values[0], values[1]) or _equal(values[1], values[2]) or _equal(values[0], values[2])            
            
            if not ok:      
                self.conflicted.append(name)          
                self.ui.attributesTable.item(idx, 0).setBackgroundColor(QtCore.Qt.yellow);
                self.ui.attributesTable.item(idx, 1).setBackgroundColor(QtCore.Qt.yellow);
                self.ui.attributesTable.item(idx, 3).setBackgroundColor(QtCore.Qt.yellow);
            else:                
                self.ui.attributesTable.setItem(idx, 3, ValueItem(values[1]));                
              
            if oursgeom is None and isinstance(values[1], BaseGeometry):                                        
                oursgeom = values[1]
            if theirsgeom is None and isinstance(values[2], BaseGeometry):                                        
                theirsgeom = values[2]
                                                                  
        self.ui.attributesTable.resizeRowsToContents()
        self.ui.attributesTable.horizontalHeader().setMinimumSectionSize(150)        
        self.ui.attributesTable.horizontalHeader().setStretchLastSection(True)                
        return (oursgeom, theirsgeom)                 
        
    def createLayers(self, oursgeom, theirsgeom):               
        settings = QtCore.QSettings()
        prjSetting = settings.value('/Projections/defaultBehaviour')
        settings.setValue('/Projections/defaultBehaviour', '')
        types = [("Point",  ptOursStyle, ptTheirsStyle),
                  ("LineString",lineOursStyle, lineTheirsStyle), 
                  ("Polygon", polygonOursStyle, polygonTheirsStyle)]                                            
        if oursgeom is not None:
            qgsgeom = QgsGeometry.fromWkt(str(oursgeom))
            geomtype = types[int(qgsgeom.type())][0]                                        
            if hasattr(oursgeom, "crs"):
                targetCrs = self.mapCanvas.mapRenderer().destinationCrs()
                crsTransform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(oursgeom.crs), targetCrs) 
                qgsgeom.transform(crsTransform)                            
            style = types[int(qgsgeom.type())][1]                     
            self.oursLayer = QgsVectorLayer(geomtype, "ours", "memory")
            pr = self.oursLayer.dataProvider()    
            feat = QgsFeature()
            feat.setGeometry(qgsgeom)
            pr.addFeatures([feat])
            self.oursLayer.loadNamedStyle(style)                    
            self.oursLayer.updateExtents()
            #this is to correct a problem with memory layers in qgis 2.2
            self.oursLayer.selectAll()            
            self.oursLayer.setExtent(self.oursLayer.boundingBoxOfSelected())
            self.oursLayer.invertSelection()                                                          
            QgsMapLayerRegistry.instance().addMapLayer(self.oursLayer, False)
        else:
            self.oursLayer = None                                                                                                
        if theirsgeom is not None:
            qgsgeom = QgsGeometry.fromWkt(str(theirsgeom))
            geomtype = types[int(qgsgeom.type())][0]            
            if hasattr(theirsgeom, "crs"):
                targetCrs = self.mapCanvas.mapRenderer().destinationCrs()
                crsTransform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(theirsgeom.crs), targetCrs) 
                qgsgeom.transform(crsTransform)             
            style = types[int(qgsgeom.type())][2]                     
            self.theirsLayer = QgsVectorLayer(geomtype, "theirs", "memory")
            pr = self.theirsLayer.dataProvider()    
            feat = QgsFeature()
            feat.setGeometry(qgsgeom)
            pr.addFeatures([feat])    
            self.theirsLayer.loadNamedStyle(style)                
            self.theirsLayer.updateExtents()
            #this is to correct a problem with memory layers in qgis 2.2
            self.theirsLayer.selectAll()            
            self.theirsLayer.setExtent(self.theirsLayer.boundingBoxOfSelected())
            self.theirsLayer.invertSelection()                                                             
            QgsMapLayerRegistry.instance().addMapLayer(self.theirsLayer, False)
        else:
            self.theirsLayer = None                         
        settings.setValue('/Projections/defaultBehaviour', prjSetting)   
      
    def showGeoms(self):  
        checks = [self.ui.showOursCheck, self.ui.showTheirsCheck]    
        layers = [self.oursLayer,  self.theirsLayer]        
        toShow = []
        for lay, chk in zip(layers, checks):
            if lay is not None and chk.isChecked():
                toShow.append(lay)        
        if len(toShow) > 0 and self.baseLayer is not None:
            toShow.append(self.baseLayer)
        self.mapCanvas.setRenderFlag(False)  
        self.mapCanvas.setLayerSet([QgsMapCanvasLayer(layer) for layer in toShow])            
        self.mapCanvas.setRenderFlag(True)
        

    def closePressed(self): 
        self.cleanCanvas()            
        self.close()        


class ValueItem(QtGui.QTableWidgetItem):
    
    def __init__(self, value):
        QtGui.QTableWidgetItem.__init__(self)
        self.value = value
        s = "" if value is None else unicode(value)
        self.setText(s)
        self.setFlags(QtCore.Qt.ItemIsEnabled)
        
        
class ConflictItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, path, versions):
        QtGui.QTreeWidgetItem.__init__(self)
        feature = os.path.basename(path)
        self.setText(0, feature)
        self.setIcon(0, featureIcon)
        self.path = path        
        self.versions = versions
        self.ours = versions[0]
        self.theirs = versions[1]
        