import os
import logging
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from geogit.ui.diffviewerdialog import Ui_DiffViewerDialog 
from geogit.gui.dialogs.geogitref import RefPanel
from geogitpy.diff import TYPE_ADDED, TYPE_MODIFIED
from geogit.tools.utils import tempFilenameInTempFolder
from geogitpy import geogit
from geogitpy.geogitexception import GeoGitException
from geogitpy.commit import Commit
from shapely.geometry.base import BaseGeometry
from geogit import config

_logger = logging.getLogger("geogitpy")

resourcesPath = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "resources")        
ptBeforeStyle = os.path.join(resourcesPath, "pt_before.qml")
ptAfterStyle = os.path.join(resourcesPath, "pt_after.qml")
lineBeforeStyle = os.path.join(resourcesPath, "line_before.qml")
lineAfterStyle = os.path.join(resourcesPath, "line_after.qml")
polygonBeforeStyle = os.path.join(resourcesPath, "polygon_before.qml")
polygonAfterStyle = os.path.join(resourcesPath, "polygon_after.qml")

layerIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "layer_group.gif"))
featureIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "geometry.png"))

class DiffViewerDialog(QtGui.QDialog):
    
    CHANGES_THRESHOLD = 300
        
    def __init__(self, repo, refa, refb, path = None):
        QtGui.QDialog.__init__(self, config.iface.mainWindow(), 
                               QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.repo = repo
        self.oldLayerId = None
        self.newLayerId = None
        self._baseLayer = None
        self.currentPath = None        
        
        if (isinstance(refa, Commit) and isinstance(refb, Commit) 
                and refa.committerdate > refb.committerdate):
            refa, refb = refb, refa
        
        self.ui = Ui_DiffViewerDialog()
        self.ui.setupUi(self)
        
        self.setWindowFlags(self.windowFlags() |
                              QtCore.Qt.WindowSystemMenuHint |
                              QtCore.Qt.WindowMinMaxButtonsHint)
        
        advancedUi = config.getConfigValue(config.GENERAL, config.ADVANCED_UI) 
        self.commit1 = refa
        self.commit1Panel = RefPanel(self.repo, refa, onlyCommits = not advancedUi)
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.commit1Panel)
        self.ui.commit1Widget.setLayout(layout)                
        self.commit2 = refb
        self.commit2Panel = RefPanel(self.repo, refb, onlyCommits = not advancedUi)
        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(self.commit2Panel)
        self.ui.commit2Widget.setLayout(layout)            
        self.commit1Panel.refChanged.connect(self.refsHaveChanged)
        self.commit2Panel.refChanged.connect(self.refsHaveChanged)
                               
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(0)
        horizontalLayout.setMargin(0)   
        self.splitMapCanvas1 = QgsMapCanvas()        
        self.splitMapCanvas1.setCanvasColor(QtCore.Qt.white)    
        settings = QtCore.QSettings()
        self.splitMapCanvas1.enableAntiAliasing(settings.value( "/qgis/enable_anti_aliasing", False, type=bool))
        self.splitMapCanvas1.useImageToRender(settings.value( "/qgis/use_qimage_to_render", False, type=bool))
        self.splitMapCanvas1.mapRenderer().setProjectionsEnabled(True)        
        action = settings.value("/qgis/wheel_action", 0, type=float)
        zoomFactor = settings.value("/qgis/zoom_factor", 2, type=float)
        self.splitMapCanvas1.setWheelAction(QgsMapCanvas.WheelAction(action), zoomFactor)
        horizontalLayout.addWidget(self.splitMapCanvas1)
        self.ui.splitMapWidget.setLayout(horizontalLayout)
        self.panTool1 = QgsMapToolPan(self.splitMapCanvas1)
                
        horizontalLayout2 = QtGui.QHBoxLayout()
        horizontalLayout2.setSpacing(0)
        horizontalLayout2.setMargin(0)   
        self.splitMapCanvas2 = QgsMapCanvas()        
        self.splitMapCanvas2.setCanvasColor(QtCore.Qt.white)    
        self.splitMapCanvas2.enableAntiAliasing(settings.value( "/qgis/enable_anti_aliasing", False, type=bool))
        self.splitMapCanvas2.useImageToRender(settings.value( "/qgis/use_qimage_to_render", False, type=bool))
        self.splitMapCanvas2.mapRenderer().setProjectionsEnabled(True)
        action = settings.value("/qgis/wheel_action", 0, type=float)
        zoomFactor = settings.value("/qgis/zoom_factor", 2, type=float)        
        self.splitMapCanvas2.setWheelAction(QgsMapCanvas.WheelAction(action), zoomFactor)
        horizontalLayout2.addWidget(self.splitMapCanvas2)
        self.ui.splitMapWidget2.setLayout(horizontalLayout2)
        self.panTool2 = QgsMapToolPan(self.splitMapCanvas2)         
        
        horizontalLayout3 = QtGui.QHBoxLayout()
        horizontalLayout3.setSpacing(0)
        horizontalLayout3.setMargin(0)   
        self.singleMapCanvas = QgsMapCanvas()        
        self.singleMapCanvas.setCanvasColor(QtCore.Qt.white)    
        self.singleMapCanvas.enableAntiAliasing(settings.value( "/qgis/enable_anti_aliasing", False, type=bool))
        self.singleMapCanvas.useImageToRender(settings.value( "/qgis/use_qimage_to_render", False, type=bool))
        self.singleMapCanvas.mapRenderer().setProjectionsEnabled(True)
        action = settings.value("/qgis/wheel_action", 0, type=float)
        zoomFactor = settings.value("/qgis/zoom_factor", 2, type=float)
        self.singleMapCanvas.setWheelAction(QgsMapCanvas.WheelAction(action), zoomFactor)        
        horizontalLayout3.addWidget(self.singleMapCanvas)
        self.ui.singleMapWidget.setLayout(horizontalLayout3) 
        self.panTool3 = QgsMapToolPan(self.singleMapCanvas)
                
        self.panAndSelectTool1 = MapToolPanAndSelect(self.splitMapCanvas1, self)        
        self.panAndSelectTool2 = MapToolPanAndSelect(self.splitMapCanvas2, self)        
        self.panAndSelectTool3 = MapToolPanAndSelect(self.singleMapCanvas, self)        
        
        def _setExtentToLayer(canvas):
            if canvas.layerCount() > 0:
                canvas.setExtent(canvas.layer(0).extent())
                canvas.refresh()                
        self.ui.zoomToCommit1Button.clicked.connect(lambda: _setExtentToLayer(self.splitMapCanvas1))        
        self.ui.zoomToCommit2Button.clicked.connect(lambda: _setExtentToLayer(self.splitMapCanvas2))
        self.ui.zoomToSingleMapButton.clicked.connect(lambda: _setExtentToLayer(self.singleMapCanvas))
        
        self.ui.featuresTreeWidget.itemExpanded.connect(self.treeItemExpanded)

        self.computeDiffs()
        
        if refa is not None and refb is not None and path is not None:
            self.selectPath(path)
            
        self.ui.featuresTreeWidget.itemClicked.connect(self.treeItemClicked)
        self.ui.featuresTreeWidget.itemDoubleClicked.connect(lambda: self.treeItemDoubleClicked)
        
        def _toggleBaseLayer(state, canvas):
            if state:                
                layers = [QgsMapCanvasLayer(layer) for layer in canvas.layers()]                
                if layers:
                    layers.append(QgsMapCanvasLayer(self.getBaseLayer()))
                    canvas.setLayerSet(layers)
            else:
                layers = [QgsMapCanvasLayer(layer) for layer in canvas.layers()]
                if layers:                                        
                    canvas.setLayerSet(layers[:-1])                
            
        self.ui.showLayerSplitMap1Check.stateChanged.connect(lambda: _toggleBaseLayer(
                                                    self.ui.showLayerSplitMap1Check.isChecked(), self.splitMapCanvas1))
        self.ui.showLayerSplitMap2Check.stateChanged.connect(lambda: _toggleBaseLayer(
                                                    self.ui.showLayerSplitMap2Check.isChecked(), self.splitMapCanvas2))
        self.ui.showLayerSingleMapCheck.stateChanged.connect(lambda: _toggleBaseLayer(
                                                    self.ui.showLayerSingleMapCheck.isChecked(), self.singleMapCanvas))
    
    def refsHaveChanged(self):        
        self.computeDiffs()
    
    def treeItemDoubleClicked(self, item, column):
        pass
            
    def treeItemClicked(self, item, column):
        if isinstance(item, FeatureDiffTreeItem):            
            if self.currentPath != item.diff.path:                
                self.currentPath = item.diff.path
                self.showFeatureDiffs(item.diff)
        elif isinstance(item, TreeDiffTreeItem):
            if self.currentPath != item.path:                                
                self.currentPath = item.path
                self.showTreeDiffs(item.commit1, item.commit2, item.path)         
                
    def getBaseLayer(self):
        if self._baseLayer is None:
            baseLayerFile = os.path.join(os.path.dirname(__file__), 
                                         os.pardir, os.pardir, "resources", "osm.xml")
            baseLayer = QgsRasterLayer(baseLayerFile, "base", "gdal")
            if baseLayer.isValid():
                self._baseLayer = baseLayer
                QgsMapLayerRegistry.instance().addMapLayer(self._baseLayer, False)
                            
        else:
            _logger.debug("Could not load base OSM layer")
        return self._baseLayer
        
    def showTreeDiffs(self, commit1, commit2, path):
        SINGLE_MAP = 1
        self.clearFeatureDiffs()        
        self.ui.mapTabWidget.setCurrentIndex(SINGLE_MAP)
        commit1File = os.path.join(tempFilenameInTempFolder("commit1.shp"))
        commit2File = os.path.join(tempFilenameInTempFolder("commit2.shp"))                        
        try:
            self.repo.exportdiffs(commit1, commit2, path, commit1File, True, True)
            commit1Layer = QgsVectorLayer(commit1File, "commit1", "ogr")
        except GeoGitException, e:
            commit1Layer = None
        try:
            self.repo.exportdiffs(commit1, commit2, path, commit2File, False, True)
            commit2Layer = QgsVectorLayer(commit2File, "commit2", "ogr")          
        except GeoGitException, e:
            commit2Layer = None                
                    
        styles = [(ptBeforeStyle, ptAfterStyle), 
                 (lineBeforeStyle, lineAfterStyle),
                 (polygonBeforeStyle, polygonAfterStyle)]  
        layers = []
        if commit1Layer is not None and commit1Layer.isValid():            
            self.oldLayerId = commit1Layer.id()                        
            beforeStyle, afterStyle = styles[commit1Layer.geometryType()]
            commit1Layer.loadNamedStyle(beforeStyle)
            commit1Layer.updateExtents()
            QgsMapLayerRegistry.instance().addMapLayer(commit1Layer, False)            
            self.splitMapCanvas1.setRenderFlag(False)                                    
            mapLayers = [QgsMapCanvasLayer(commit1Layer)]
            if self.ui.showLayerSplitMap1Check.isChecked():
                mapLayers.append(QgsMapCanvasLayer(self.getBaseLayer()))                           
            self.splitMapCanvas1.setLayerSet(mapLayers)                      
            self.splitMapCanvas1.setExtent(commit1Layer.extent())
            self.splitMapCanvas1.setRenderFlag(True)                         
            layers.append(commit1Layer)
        if commit2Layer is not None and commit2Layer.isValid():
            beforeStyle, afterStyle = styles[commit2Layer.geometryType()]             
            self.newLayerId = commit2Layer.id()                                  
            commit2Layer.loadNamedStyle(afterStyle)
            commit2Layer.updateExtents()
            QgsMapLayerRegistry.instance().addMapLayer(commit2Layer, False)
            self.splitMapCanvas2.setRenderFlag(False)                                    
            mapLayers = [QgsMapCanvasLayer(commit2Layer)]
            if self.ui.showLayerSplitMap2Check.isChecked():
                mapLayers.append(QgsMapCanvasLayer(self.getBaseLayer()))                           
            self.splitMapCanvas2.setLayerSet(mapLayers)                        
            self.splitMapCanvas2.setExtent(commit2Layer.extent())
            self.splitMapCanvas2.setRenderFlag(True)  
            layers.append(commit2Layer)
        
        settings = QtCore.QSettings()
        prjSetting = settings.value('/Projections/defaultBehaviour')
        settings.setValue('/Projections/defaultBehaviour', '')
        if layers:
            extent = self.getFullExtent(layers)
            if self.ui.showLayerSingleMapCheck.isChecked():
                layers.append(self.getBaseLayer())
            self.singleMapCanvas.setRenderFlag(False)  
            self.singleMapCanvas.setLayerSet([QgsMapCanvasLayer(layer) for layer in layers])
            self.singleMapCanvas.setExtent(extent)
            self.singleMapCanvas.setRenderFlag(True)
        settings.setValue('/Projections/defaultBehaviour', prjSetting)
        
        self.singleMapCanvas.setMapTool(self.panAndSelectTool3)
        self.splitMapCanvas1.setMapTool(self.panAndSelectTool1) 
        self.splitMapCanvas2.setMapTool(self.panAndSelectTool2)
        
    def getFullExtent(self, layers):
        extent = layers[0].extent()
        for layer in layers[1:]:
            extent.combineExtentWith(layer.extent())
        return extent
        
    def featureClickedInCanvas(self, canvas, fid):
        layers = canvas.layers()
        if len(layers) == 0:
            return
        layer = layers[0]
        layer.setSelectedFeatures([fid])
        canvas.refresh()
        diff = self.repo.featurediff(self.commit1.ref, self.commit2.ref, self.currentPath + "/" + fid)
        self.ui.attributesTable.setRowCount(0)
        self.showFeatureAttributes(diff)
        
                    
    def showFeatureDiffs(self, diff):
        self.clearFeatureDiffs()
        oldgeom, newgeom = self.showFeatureAttributes(diff)
        self.showGeomDiffs(oldgeom, newgeom)

    def showFeatureAttributes(self, diff):            
        oldgeom = None
        newgeom = None
        if isinstance(diff, dict):
            featurediff = diff
        else:
            featurediff = diff.featurediff()
        self.ui.attributesTable.setRowCount(len(featurediff))        
        for idx, name in enumerate(featurediff):            
            values = featurediff[name]
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item = QtGui.QTableWidgetItem(name)
            item.setFont(font)            
            self.ui.attributesTable.setItem(idx, 1, item);
            oldValue = values[0] if values[0] is not None else ""
            newValue = values[1] if values[1] is not None else ""
            self.ui.attributesTable.setItem(idx, 0, QtGui.QTableWidgetItem(unicode(oldValue)));            
            self.ui.attributesTable.setItem(idx, 2, QtGui.QTableWidgetItem(unicode(newValue)));
            color = None
            if values[0] is None:
                color = QtCore.Qt.green
            elif values[1] is None:
                color = QtCore.Qt.red
            elif values[0] != values[1]:
                color = QtCore.Qt.yellow
            if color is not None:                
                    self.ui.attributesTable.item(idx, 0).setBackgroundColor(color);
                    self.ui.attributesTable.item(idx, 2).setBackgroundColor(color); 
            if oldgeom is None and isinstance(oldValue, BaseGeometry):                                        
                oldgeom = oldValue
            if newgeom is None and isinstance(newValue, BaseGeometry):                                        
                newgeom = newValue
                                                                  
        self.ui.attributesTable.resizeRowsToContents()
        self.ui.attributesTable.horizontalHeader().setMinimumSectionSize(150)        
        self.ui.attributesTable.horizontalHeader().setStretchLastSection(True)        
        return oldgeom, newgeom                   
        
    def showGeomDiffs(self, oldgeom, newgeom): 
        SPLIT_MAP = 0
        self.ui.mapTabWidget.setCurrentIndex(SPLIT_MAP)
        settings = QtCore.QSettings()
        prjSetting = settings.value('/Projections/defaultBehaviour')
        settings.setValue('/Projections/defaultBehaviour', '')
        types = [("Point", ptBeforeStyle, ptAfterStyle), 
                 ("LineString", lineBeforeStyle, lineAfterStyle),
                 ("Polygon", polygonBeforeStyle, polygonAfterStyle)]                            
        layers = []
        if oldgeom is not None:
            qgsgeom = QgsGeometry.fromWkt(str(oldgeom))
            geomtype, beforeStyle, afterStyle = types[int(qgsgeom.type())]                        
            if hasattr(oldgeom, "crs"):
                targetCrs = self.splitMapCanvas1.mapRenderer().destinationCrs()
                crsTransform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(oldgeom.crs), targetCrs) 
                qgsgeom.transform(crsTransform)                                 
            oldLayer = QgsVectorLayer(geomtype, "Old", "memory")
            pr = oldLayer.dataProvider()    
            feat = QgsFeature()
            feat.setGeometry(qgsgeom)
            pr.addFeatures([feat])               
            oldLayer.updateExtents() 
            
            #this is to correct a problem with memory layers in qgis 2.2
            oldLayer.selectAll()            
            oldLayer.setExtent(oldLayer.boundingBoxOfSelected())
            oldLayer.invertSelection()
                    
            self.oldLayerId = oldLayer.id()                        
            oldLayer.loadNamedStyle(beforeStyle)
            self.splitMapCanvas1.setRenderFlag(False)
            mapLayers = [QgsMapCanvasLayer(oldLayer)]
            if self.ui.showLayerSplitMap1Check.isChecked():
                mapLayers.append(QgsMapCanvasLayer(self.getBaseLayer()))                           
            self.splitMapCanvas1.setLayerSet(mapLayers)                                                        
            QgsMapLayerRegistry.instance().addMapLayer(oldLayer, False)            
            self.splitMapCanvas1.setExtent(oldLayer.extent())
            self.splitMapCanvas1.setRenderFlag(True)            
            layers.append(oldLayer)    
        if newgeom is not None: 
            qgsgeom = QgsGeometry.fromWkt(str(newgeom))
            geomtype, beforeStyle, afterStyle = types[int(qgsgeom.type())]
            if hasattr(newgeom, "crs"):
                targetCrs = self.splitMapCanvas2.mapRenderer().destinationCrs()
                crsTransform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(newgeom.crs), targetCrs) 
                qgsgeom .transform(crsTransform)               
            newLayer = QgsVectorLayer(geomtype, "New", "memory")
            pr = newLayer.dataProvider()    
            feat = QgsFeature()
            feat.setGeometry(qgsgeom)
            pr.addFeatures([feat])  
            newLayer.updateExtents() 
            
            #this is to correct a problem with memory layers in qgis 2.2
            newLayer.selectAll()            
            newLayer.setExtent(newLayer.boundingBoxOfSelected())
            newLayer.invertSelection()
                                
            self.newLayerId = newLayer.id()            
            newLayer.loadNamedStyle(afterStyle)
            self.splitMapCanvas2.setRenderFlag(False)
            mapLayers = [QgsMapCanvasLayer(newLayer)]
            if self.ui.showLayerSplitMap2Check.isChecked():
                mapLayers.append(QgsMapCanvasLayer(self.getBaseLayer()))                           
            self.splitMapCanvas2.setLayerSet(mapLayers)            
            QgsMapLayerRegistry.instance().addMapLayer(newLayer, False)
            self.splitMapCanvas2.setExtent(newLayer.extent())
            self.splitMapCanvas2.setRenderFlag(True)
            self.splitMapCanvas2.updateMap()
            self.splitMapCanvas2.refresh()
            layers.append(newLayer)        
        if layers:
            extent = self.getFullExtent(layers)
            if self.ui.showLayerSingleMapCheck.isChecked():
                layers.append(self.getBaseLayer())
            self.singleMapCanvas.setRenderFlag(False)  
            self.singleMapCanvas.setLayerSet([QgsMapCanvasLayer(layer) for layer in layers])
            self.singleMapCanvas.setExtent(extent)
            self.singleMapCanvas.setRenderFlag(True)
        else:
            self.singleMapCanvas.setLayerSet([])
        settings.setValue('/Projections/defaultBehaviour', prjSetting)       
        
        self.singleMapCanvas.setMapTool(self.panTool3)
        self.splitMapCanvas1.setMapTool(self.panTool1) 
        self.splitMapCanvas2.setMapTool(self.panTool2)     
        
    def computeDiffs(self):
        self.commit1 = self.commit1Panel.getRef()
        self.commit2 = self.commit2Panel.getRef()
        commit1 = self.commit1.ref
        commit2 = self.commit2.ref    
        diffs = self.repo.difftreestats(commit1, commit2)
        self.ui.featuresTreeWidget.clear()
        total = 0
        for path, counts in diffs.iteritems():        
            pathItem = TreeDiffTreeItem(path, counts, commit1, commit2)            
            subtotal = sum(counts)
            total += subtotal
            if subtotal > self.CHANGES_THRESHOLD: 
                item = QtGui.QTreeWidgetItem([str(counts[0]) + " features added"])
                item.setTextColor(0, QtGui.QColor(0, 200, 0))
                pathItem.addChild(item)            
                item = QtGui.QTreeWidgetItem([str(counts[1]) + " features removed"])
                item.setTextColor(0, QtGui.QColor(200, 0, 0))
                pathItem.addChild(item)
                item = QtGui.QTreeWidgetItem([str(counts[2]) + " features modified"])
                item.setTextColor(0, QtGui.QColor(218, 135, 62))
                pathItem.addChild(item)
            self.ui.featuresTreeWidget.addTopLevelItem(pathItem)
            
        self.clearFeatureDiffs()
                    
        
    def treeItemExpanded(self, item):
        if item is None or item.childCount():            
            return                
        diffs = self.repo.diff(item.commit1, item.commit2, item.path)        
                             
        for diff in diffs:
            featureItem = FeatureDiffTreeItem(diff)
            item.addChild(featureItem)         
        
    def clearFeatureDiffs(self):        
        self.ui.attributesTable.setRowCount(0) 
        self.singleMapCanvas.setLayerSet([])
        self.splitMapCanvas1.setLayerSet([])
        self.splitMapCanvas2.setLayerSet([])
        if self.oldLayerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.oldLayerId)  
            self.oldLayerId = None                
        if self.newLayerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.newLayerId)
            self.newLayerId = None            
    
    def selectPath(self, path):    
        for i in range(self.ui.featuresTreeWidget.topLevelItemCount()):
            item = self.ui.featuresTreeWidget.topLevelItem(i)
            if item.path == path:
                self.treeItemClicked(item, 0)
                return
            if path.startswith(item.path):
                self.treeItemExpanded(item)
                for j in xrange(item.childCount()):
                    subitem = item.child(j) 
                    if subitem.path == path:
                        item.setExpanded(True)
                        self.treeItemClicked(subitem, 0)
                        return

        
    def reject(self):
        QtGui.QDialog.reject(self)
        if self.oldLayerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.oldLayerId)                
        if self.newLayerId:
            QgsMapLayerRegistry.instance().removeMapLayer(self.newLayerId)
        if self.getBaseLayer():
            QgsMapLayerRegistry.instance().removeMapLayer(self.getBaseLayer().id())                            
        
class TreeDiffTreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, path, counts, commit1, commit2):                
        QtGui.QTreeWidgetItem.__init__(self)
        self.commit1 = commit1
        self.commit2 = commit2
        self.path = path
        self.counts = counts 
        self.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)            
        self.setText(0, path + " [+%i/-%i/~%i]" % counts)
        self.setIcon(0, layerIcon)
                
class FeatureDiffTreeItem(QtGui.QTreeWidgetItem): 
    def __init__(self, diff): 
        QtGui.QTreeWidgetItem.__init__(self) 
        self.diff = diff  
        self.path = diff.path                                
        self.setText(0, os.path.basename(diff.path))        
        def colorFromType(t):
            if t == TYPE_ADDED:
                return QtGui.QColor(0, 200, 0)
            elif t == TYPE_MODIFIED:
                return QtGui.QColor(218, 135, 62)                   
            else:
                return QtGui.QColor(200, 0, 0)

        self.setTextColor(0, colorFromType(diff.type()))
        self.setIcon(0, featureIcon)         
        
class MapToolPanAndSelect(QgsMapToolPan):
  
   
    def __init__(self, canvas, viewer):
        self.canvas = canvas
        self.viewer = viewer
        QgsMapTool.__init__(self, self.canvas)
        self.setCursor(QtCore.Qt.CrossCursor)

    def canvasPressEvent(self, e):
        layers = self.canvas.layers()
        if len(layers) == 0:
            return
        layer = layers[0]
        
        point = self.toMapCoordinates(e.pos())
        searchRadius = self.canvas.extent().width() * .01;
        r = QgsRectangle()
        r.setXMinimum(point.x() - searchRadius);
        r.setXMaximum(point.x() + searchRadius);
        r.setYMinimum(point.y() - searchRadius);
        r.setYMaximum(point.y() + searchRadius);
    
        r = self.toLayerCoordinates(layer, r);
        
        fit = layer.getFeatures(QgsFeatureRequest().setFilterRect(r).setFlags(QgsFeatureRequest.ExactIntersect));
        try:
            fid = fit.next()["geogit_fid"]            
            self.viewer.featureClickedInCanvas(self.canvas, fid)                
        except StopIteration, e:                
            pass

            
