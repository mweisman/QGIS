import os
import logging
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from geogit.ui.mergedialog import Ui_MergeDialog
from geogitpy.geogitexception import GeoGitConflictException
from geogitpy import geogit
from geogitpy.feature import Feature
from shapely.geometry.base import BaseGeometry
from geogit import config

BASEMAP_NONE = 0
BASEMAP_OSM = 1
BASEMAP_GOOGLE = 2

resourcesPath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "resources")        
ptOriginStyle = os.path.join(resourcesPath, "pt_origin.qml")
ptOursStyle = os.path.join(resourcesPath, "pt_ours.qml")
ptTheirsStyle = os.path.join(resourcesPath, "pt_theirs.qml")
lineOriginStyle = os.path.join(resourcesPath, "line_origin.qml")
lineOursStyle = os.path.join(resourcesPath, "line_ours.qml")
lineTheirsStyle = os.path.join(resourcesPath, "line_theirs.qml")
polygonOriginStyle = os.path.join(resourcesPath, "polygon_origin.qml")
polygonOursStyle = os.path.join(resourcesPath, "polygon_ours.qml")
polygonTheirsStyle = os.path.join(resourcesPath, "polygon_theirs.qml")

layerIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "layer_group.gif"))
featureIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "geometry.png"))

SELECT_BRANCH = "[Select a branch]"

_logger = logging.getLogger("geogitpy")

class MergeDialog(QtGui.QDialog):
    def __init__(self, repo):
        QtGui.QDialog.__init__(self, config.iface.mainWindow(), QtCore.Qt.WindowMinMaxButtonsHint |
                               QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.repo = repo   
        self.ref = None             
        self.ui = Ui_MergeDialog()
        self.ui.setupUi(self)
        self.resize(650, 150)        
        self.ui.splitterChanges.setVisible(False)        
        self.ui.buttonBox.rejected.connect(self.closePressed)
        self.ui.mergeButton.setEnabled(False)
        self.ui.viewChangesButton.setEnabled(False)
        self.ui.viewChangesButton.clicked.connect(self.viewChangesPressed)
        self.ui.mergeButton.clicked.connect(self.mergeButtonPressed)
        self.ui.zoomButton.clicked.connect(self.zoomPressed)        
        self.ui.changesTree.itemClicked.connect(self.changesTreeItemClicked)         
        self.ui.baseMapCombo.currentIndexChanged.connect(self.baseMapChanged)
        branches = [SELECT_BRANCH]
        branches.extend([b for b in repo.branches.keys()])
        self.ui.branchToMergeBox.addItems(branches)
        self.ui.branchToMergeBox.currentIndexChanged.connect(self.branchToMergeChanged)
        
        def refreshMap():            
            #self.mapCanvas.setLayerSet([])
            self.showGeoms()
        self.ui.showTheirsCheck.stateChanged.connect(refreshMap) 
        self.ui.showOriginCheck.stateChanged.connect(refreshMap)
        self.ui.showOursCheck.stateChanged.connect(refreshMap)
        
        self.lastSelectedItem = None
        self.currentPath = None
        self.theirsLayer = None
        self.originLayer = None
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
        
        self.ui.changesTree.itemExpanded.connect(self.treeItemExpanded)    
        

    def treeItemExpanded(self, item):
        if not isinstance(item, ConflictedPathTreeItem):            
            return      
        if item.childCount() > 0:
            return          
        headDiffsFeaturePaths = set(d.path for d in self.repo.diff(item.ancestor, geogit.HEAD, item.path))
        toMergeDiffsFeaturePaths = set(d.path for d in self.repo.diff(item.toMerge, geogit.HEAD, item.path))
        bothBranchesFeaturePaths = headDiffsFeaturePaths.intersection(toMergeDiffsFeaturePaths)                                         
        for path in bothBranchesFeaturePaths:
            featureItem = ConflictedFeatureTreeItem(path, item.toMerge, item.ancestor)
            item.addChild(featureItem)  
            
    def branchToMergeChanged(self):
        toMerge = self.ui.branchToMergeBox.currentText()
        if toMerge == SELECT_BRANCH:
            self.ui.mergeButton.setEnabled(False)
            self.ui.viewChangesButton.setEnabled(False)
            return
        self.ui.changesTree.clear()        
        ancestor = self.repo.commonancestor(geogit.HEAD, toMerge).ref
        diffsHead = self.repo.difftreestats(geogit.HEAD, ancestor)
        diffsToMerge = self.repo.difftreestats(toMerge, ancestor)
        toMergeItem = QtGui.QTreeWidgetItem(["Changed in branch to merge"])
        self.ui.changesTree.addTopLevelItem(toMergeItem)
        headItem = QtGui.QTreeWidgetItem(["Changed in current branch"])
        self.ui.changesTree.addTopLevelItem(headItem)
        bothBranchesItem = QtGui.QTreeWidgetItem(["Changed in both branches"])
        self.ui.changesTree.addTopLevelItem(bothBranchesItem)        
        
        for path, counts in diffsHead.iteritems():
            if path in diffsToMerge:
                pathItem = ConflictedPathTreeItem(path, toMerge, ancestor)
                bothBranchesItem.addChild(pathItem)
            else:
                pathItem = PathTreeItem(path, counts)
                headItem.addChild(pathItem)
        for path, counts in diffsToMerge.iteritems():
            if path not in diffsHead:
                pathItem = PathTreeItem(path, counts)
                toMergeItem.addChild(pathItem)
                
        self.clearFeatureDiffs()  
        self.cleanCanvas()
        self.ui.mergeButton.setEnabled(True)
        self.ui.viewChangesButton.setEnabled(True)

    def clearFeatureDiffs(self):
        self.ui.attributesTable.setRowCount(0)  
        
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
    
    def changesTreeItemClicked(self):                          
        item = self.ui.changesTree.selectedItems()[0]
        if self.lastSelectedItem == item:
            return
        self.lastSelectedItem = item
        if isinstance(item, ConflictedFeatureTreeItem):
            self.currentPath = item.path
            self.updateCurrentPath(item.path, item.toMerge, item.ancestor)             
        
    def updateCurrentPath(self, path, toMerge, ancestor):
        self.cleanCanvas()
        versions = [Feature(self.repo, toMerge, path), Feature(self.repo, geogit.HEAD, path), 
                    Feature(self.repo, ancestor, path)]
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
        #self.ui.attributesTable.setRowCount(0)        
        self.mapCanvas.setLayerSet([])        
        layers = [self.oursLayer, self.originLayer, self.theirsLayer, self.baseLayer]
        for layer in layers:
            if layer is not None:
                QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
        self.oursLayer = None
        self.originLayer = None
        self.theirsLayer = None
        self.baseLayer = None                     
   
    
    def showFeatureAttributes(self, versions):         
        oursgeom = None
        theirsgeom = None
        origingeom = None
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
            self.ui.attributesTable.setItem(idx, 0, item);
            for i, v in enumerate(values):            
                v = v or ""
                self.ui.attributesTable.setItem(idx, i+1, QtGui.QTableWidgetItem(str(v)));                                                                          

            def _equal(a, b):     
                if isinstance(a, BaseGeometry) and isinstance(b, BaseGeometry):                    
                    return a.to_wkt() == b.to_wkt()                    
                else:
                    return a ==b
                                    
            ok =  _equal(values[0], values[1]) or _equal(values[1], values[2]) or _equal(values[0], values[2])            
                                         
            if not ok:                           
                self.ui.attributesTable.item(idx, 1).setBackgroundColor(QtCore.Qt.yellow);
                self.ui.attributesTable.item(idx, 2).setBackgroundColor(QtCore.Qt.yellow);
                 
            if origingeom is None and isinstance(values[0], BaseGeometry):                                        
                origingeom =values[0]                 
            if oursgeom is None and isinstance(values[1], BaseGeometry):                                        
                oursgeom = values[1]
            if theirsgeom is None and isinstance(values[2], BaseGeometry):                                        
                theirsgeom = values[2]
                                                                  
        self.ui.attributesTable.resizeRowsToContents()
        self.ui.attributesTable.horizontalHeader().setMinimumSectionSize(150)        
        self.ui.attributesTable.horizontalHeader().setStretchLastSection(True)                
        return (origingeom, oursgeom, theirsgeom)                 
        
    def createLayers(self, origingeom, oursgeom, theirsgeom):               
        settings = QtCore.QSettings()
        prjSetting = settings.value('/Projections/defaultBehaviour')
        settings.setValue('/Projections/defaultBehaviour', '')
        types = [("Point", ptOriginStyle, ptOursStyle, ptTheirsStyle),
                  ("LineString", lineOriginStyle, lineOursStyle, lineTheirsStyle), 
                  ("Polygon", polygonOriginStyle, polygonOursStyle, polygonTheirsStyle)]                                
        if origingeom is not None:
            qgsgeom = QgsGeometry.fromWkt(str(origingeom))
            geomtype = types[int(qgsgeom.type())][0]            
            if hasattr(origingeom, "crs"):
                targetCrs = self.mapCanvas.mapRenderer().destinationCrs()
                crsTransform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(origingeom.crs), targetCrs) 
                qgsgeom.transform(crsTransform)             
            style = types[int(qgsgeom.type())][1]                  
            self.originLayer = QgsVectorLayer(geomtype, "origin", "memory")
            pr = self.originLayer.dataProvider()    
            feat = QgsFeature()
            feat.setGeometry(qgsgeom)
            pr.addFeatures([feat])          
            self.originLayer.loadNamedStyle(style)     
            self.originLayer.updateExtents()  
            #this is to correct a problem with memory layers in qgis 2.2
            self.originLayer.selectAll()            
            self.originLayer.setExtent(self.originLayer.boundingBoxOfSelected())
            self.originLayer.invertSelection()                                                               
            QgsMapLayerRegistry.instance().addMapLayer(self.originLayer, False)  
        else:
            self.originLayer = None              
        if oursgeom is not None:
            qgsgeom = QgsGeometry.fromWkt(str(oursgeom))
            geomtype = types[int(qgsgeom.type())][0]            
            if hasattr(oursgeom, "crs"):
                targetCrs = self.mapCanvas.mapRenderer().destinationCrs()
                crsTransform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(oursgeom.crs), targetCrs) 
                qgsgeom.transform(crsTransform)                            
            style = types[int(qgsgeom.type())][2]                     
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
            style = types[int(qgsgeom.type())][3]                     
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
        checks = [self.ui.showOursCheck, self.ui.showOriginCheck, self.ui.showTheirsCheck]    
        layers = [self.oursLayer, self.originLayer, self.theirsLayer]        
        toShow = []
        for lay, chk in zip(layers, checks):
            if lay is not None and chk.isChecked():
                toShow.append(lay)        
        if len(toShow) > 0 and self.baseLayer is not None:
            toShow.append(self.baseLayer)
        self.mapCanvas.setRenderFlag(False)  
        self.mapCanvas.setLayerSet([QgsMapCanvasLayer(layer) for layer in toShow])            
        self.mapCanvas.setRenderFlag(True)
        self.mapCanvas.updateMap()
        self.mapCanvas.refresh()
        

    def closePressed(self): 
        self.cleanCanvas()
        self.ref = None            
        self.close()
        
    def viewChangesPressed(self):
        visible = self.ui.splitterChanges.isVisible()
        self.ui.splitterChanges.setVisible(not visible)
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)
        if not visible:
            #self.resize(800, 600)
            self.ui.viewChangesButton.setText("Hide changes")
            self.layout().setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        else:
            #self.resize(650, 150)
            self.ui.viewChangesButton.setText("View changes before merging >>")
        
        
                        
        
    def mergeButtonPressed(self): 
        toMerge = self.ui.branchToMergeBox.currentText()
        if toMerge == SELECT_BRANCH:
            QtGui.QMessageBox.warning(self, 'Select branch to merge',
                    "A branch must be selected to perform the merge operation",
                    QtGui.QMessageBox.Ok)
                    
        self.cleanCanvas()
        self.ref = toMerge            
        self.close()            

    
class ConflictedFeatureTreeItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, path, toMerge, ancestor):
        QtGui.QTreeWidgetItem.__init__(self)
        feature = os.path.basename(path)
        self.setText(0, feature)
        self.setIcon(0, featureIcon)
        self.path = path        
        self.toMerge = toMerge
        self.ancestor = ancestor
              
class ConflictedPathTreeItem(QtGui.QTreeWidgetItem):
    
    def __init__(self, path, toMerge, ancestor):
        QtGui.QTreeWidgetItem.__init__(self)        
        self.setText(0, path)
        self.setIcon(0, layerIcon)
        self.path = path        
        self.toMerge = toMerge
        self.ancestor = ancestor
        self.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator) 
        
class PathTreeItem(QtGui.QTreeWidgetItem): 
    
    def __init__(self, path, counts):                
        QtGui.QTreeWidgetItem.__init__(self)        
        self.path = path
        self.counts = counts                 
        self.setText(0, path + " [+%i/-%i/~%i]" % counts)
        self.setIcon(0, layerIcon)        