import os
from PyQt4 import QtGui, QtCore
from qgis.core import *
from geogit.ui.importexportdialog import Ui_ImportExportDialog
from geogit.tools import layers
from geogit.tools.layers import WrongLayerNameException
from geogit.tools.exporter import exportVectorLayer
from geogitpy.commit import Commit
from geogitpy.tree import Tree
from geogitpy import geogit
from geogit import config
from geogit.gui.dialogs.geogitref import RefPanel
from geogit.tools.layertracking import addTrackedLayer, addTrackedDatabase
from geogit.gui.dialogs.userpasswd import UserPasswordDialog
from geogitpy.geogitexception import GeoGitException

class ImportExportDialog(QtGui.QDialog):        
    
    IMPORT = 0
    EXPORT = 1
    BOTH = 2
    
    LAYER = 0
    FILE = 0
    OSM = 1
    SPATIALITE = 1
    POSTGIS = 2    
        
    def __init__(self, parent, repo, tab,  
                 ref = None, layer = None, dest = None, closeAfterOperation = False):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)        
        self.ui = Ui_ImportExportDialog()
        self.ui.setupUi(self)
        self.repo = repo
        self.closeAfterOperation = closeAfterOperation        
        self.importButton = QtGui.QPushButton("Import")
        self.importButton.clicked.connect(self.importClicked)        
        exportButton = QtGui.QPushButton("Export")
        exportButton.clicked.connect(self.exportClicked)
        self.ui.importButtonBox.addButton(self.importButton, QtGui.QDialogButtonBox.ApplyRole)
        self.ui.exportButtonBox.addButton(exportButton, QtGui.QDialogButtonBox.ApplyRole)
        self.ui.importButtonBox.rejected.connect(self.reject)
        self.ui.exportButtonBox.rejected.connect(self.reject)
        
        verticalLayout = QtGui.QVBoxLayout()
        verticalLayout.setSpacing(0)
        verticalLayout.setMargin(0)
        advancedUi = config.getConfigValue(config.GENERAL, config.ADVANCED_UI)
        self.refPanel = RefPanel(self.repo, onlyCommits = not advancedUi)
        verticalLayout.addWidget(self.refPanel)        
        self.ui.exportSnapshotWidget.setLayout(verticalLayout)
        self.ui.selectLayerFileButton.clicked.connect(self.selectLayerFile)
        self.ui.selectExportFileButton.clicked.connect(self.selectExportFile)
        self.ui.selectOsmFileButton.clicked.connect(self.selectOsmFile)
        self.ui.mappingFileButton.clicked.connect(self.selectMappingFile)
        self.ui.featureIdBox.setText("id")

        #hide bars until progress indication is fixed
        self.ui.progressBarImport.setVisible(False)        
        self.ui.progressBarExport.setVisible(False)
        
        self.ui.importTestConnectionButton.setVisible(False)
        self.ui.exportTestConnectionButton.setVisible(False)
        self.ui.importListFeatureTypesButton.setVisible(False)
        self.ui.exportListFeatureTypesButton.setVisible(False)
            
        layerNames = [layer.name() for layer in layers.getVectorLayers()]
        self.ui.importLayerComboBox.addItems(layerNames)                
        
        self.refPanel.refChanged.connect(self.snapshotHasChanged)       
        
        if tab == self.IMPORT:
            self.ui.importExportTabWidget.removeTab(self.EXPORT)
        if tab == self.EXPORT:
            self.ui.importExportTabWidget.removeTab(self.IMPORT)
            
        if ref is not None:
            self.refPanel.setRef(ref)
            
        if layer is not None:
            idx = layerNames.index(layer.name())
            self.ui.importLayerComboBox.setCurrentIndex(idx)
            
        if dest is not None:
            self.ui.destTreeBox.setText(dest)
                        
    def snapshotHasChanged(self):        
        self.ui.layersList.clear()
        tree = Tree(self.repo, self.refPanel.getRef().ref)
        for subtree in tree.trees:            
            item = TreeListItem(subtree.path)                                        
            self.ui.layersList.addItem(item)
        
    def selectLayerFile(self):        
        settings = QtCore.QSettings()        
        path = settings.value("/GeoGit/LastImportFilePath", "")        
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select import file", path, "All files (*.*)")
        if filename != "":
            self.ui.importLayerComboBox.setEditText(filename)
            settings.setValue("/GeoGit/LastImportFilePath", os.path.dirname(filename))
    
    def selectExportFile(self):
        settings = QtCore.QSettings()         
        path = settings.value("/GeoGit/LastExportFilePath", "")        
        filename = QtGui.QFileDialog.getSaveFileName(self, "Select shp file", path, "Shapefile files (*.shp)")
        if filename != "":
            self.ui.exportFileBox.setText(filename)
            settings.setValue("/GeoGit/LastExportFilePath", os.path.dirname(filename))
            
    def selectOsmFile(self):
        settings = QtCore.QSettings()        
        path = settings.value("/GeoGit/LastImportOsmPath", "")        
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select OSM file", path, "OSM files (*.xml *.osm)")
        if filename != "":
            self.ui.osmFileBox.setText(filename)
            settings.setValue("/GeoGit/LastImportOsmPath", os.path.dirname(filename))
            
    def selectMappingFile(self):
        settings = QtCore.QSettings()        
        path = settings.value("/GeoGit/LastImportOsmMappingPath", "")        
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select mapping file", path, "GeoGit OSM mapping files (*.json)")
        if filename != "":
            self.ui.mappingFileBox.setText(filename)
            settings.setValue("/GeoGit/LastImportOsmMappingPath", os.path.dirname(filename))            
    
    def importClicked(self):
        def setProgress(i):
            self.ui.progressBarImport.setValue(i)
        self.ui.featureIdBox.setStyleSheet("QLineEdit{background: white}")                
        sourceType = self.ui.importTypeWidget.currentIndex()
        add = self.ui.addCheckBox.isChecked()
        dest = self.ui.destTreeBox.text()                
        if sourceType == self.LAYER:               
            isPostGis = False
            isSpatiaLite = False
            text = self.ui.importLayerComboBox.currentText()
            layer = None
            try:                                
                layer = layers.resolveLayer(text)                                                                               
                if dest.strip() == "":
                    dest = layer.name()                     
                isPostGis = layer.dataProvider().name() == "postgres"
                isSpatiaLite = layer.dataProvider().name() == "sqlite"
                source = layer.source()
            except WrongLayerNameException, e:
                source = text          
                if dest.strip() == "":
                    dest = os.path.basename(source)
                    dest = dest[:dest.find(".")]            
            if isPostGis:
                provider = layer.dataProvider()
                uri = QgsDataSourceURI(provider.dataSourceUri())   
                password = uri.password()
                username = uri.username()
                if not password or not username:
                    dlg = UserPasswordDialog(self)
                    dlg.exec_()
                    if dlg.user is None:
                        return
                    username = dlg.user
                    password = dlg.password                                                                                                       
                self.repo.importpg(uri.database(), username, password, uri.table(), 
                              uri.schema(), uri.host(), uri.port(), add, dest)    
            elif isSpatiaLite:
                provider = layer.dataProvider()
                uri = QgsDataSourceURI(provider.dataSourceUri())                                                                                     
                self.repo.importsl(uri.database(), uri.table(), add, dest)                
            else:
                idAttribute = self.ui.featureIdBox.text()                
                if idAttribute == "":
                    self.ui.featureIdBox.setStyleSheet("QLineEdit{background: yellow}")
                    return          

                if layer is None: 
                    layer = QgsVectorLayer(source, "layer", "ogr")                                                
                    if not layer.isValid() or layer.type() != QgsMapLayer.VectorLayer:
                        raise GeoGitException ("Error reading file {} or it is not a valid vector layer file".format(source))                    

                addId = False
                hasField = False
                fields = layer.pendingFields().toList()        
                for field in fields:
                    if field.name().lower() == idAttribute.lower():
                        hasField = True
                        idAttribute = field.name()
                        break                
                if not hasField and idAttribute.lower() != "id":
                    QtGui.QMessageBox.warning(self, "Wrong value", "The specified id field is not found in the layer to import")
                    return
                if idAttribute.lower() != "id" and idAttribute.lower() != "fid":
                    ret = QtGui.QMessageBox.warning(self, "Warning", "In order to maximize functionality, the imported layer\n" 
                                                        "should have the feature identifier in a field called 'id'.\n"                                                        
                                                        "If your layer doesn't have an 'id' field, the importer can\n"
                                                        "create one automatically for you. Go back and use 'id' as field,\n"
                                                        "and you will be prompted to confirm the creation of the field.\n\n"
                                                        "Are you sure you want to use %s as the feature ID field?" % idAttribute,
                                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                    if ret == QtGui.QMessageBox.No:
                        return
                else:
                    if not hasField:
                        ret = QtGui.QMessageBox.warning(self, "Warning", "The layer to import doesn't have an 'id' field\n"
                                                        "You need to create an 'id' field before importing\n"
                                                        "Do you want GeoGit to create one for you before importing?",
                                                        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                        if ret == QtGui.QMessageBox.No:
                            return    
                        else:
                            addId = True
                exported = exportVectorLayer(layer, addId)                                                    
                self.repo.importshp(exported, add, dest, idAttribute)                     
            if addId:
                QtGui.QMessageBox.warning(self, "Warning", "A feature ID field has been added to the layer before importing.\n"
                                                                "If you want to edit the data in the repo, do not edit the original\n"
                                                                "layer without the ID field. Instead, export from the repository and\n"
                                                                "make your edits on the exported layer, so they can be synchronized\n"
                                                                "with the copy in the repository",  QtGui.QMessageBox.Ok)
            else:
                addTrackedLayer(self.repo.url, source, dest)            
        elif sourceType == self.OSM:
            mapping = self.ui.mappingFileBox.text().strip()
            if mapping == "":
                mapping = None
            source = self.ui.osmFileBox.text()
            self.repo.importosm(source, add)
        elif sourceType == self.POSTGIS:
            host = self.ui.pgImportHostBox.text().strip()
            host = "localhost" if host == "" else host
            database = self.ui.pgImportDatabaseBox.text().strip()
            database = "database" if database == "" else database
            user = self.ui.pgImportUserBox.text().strip()
            user = "postgres" if user == "" else user
            password = self.ui.pgImportPasswordBox.text().strip()
            password = "postgres" if password == "" else password
            port = self.ui.pgImportPortBox.text().strip()
            port = "5432" if port == "" else port
            schema = self.ui.pgImportSchemaBox.text().strip()
            schema = "public" if schema == "" else schema            
            table = self.ui.pgImportTablesBox.text().strip()
            table = None if table == "" else table
            if dest.strip() == "":
                dest = None
            self.repo.importpg(database, user, password, table, schema, host, port, add, dest)
            if table is None:
                addTrackedDatabase(self.repo.url, host, database, port, schema, dest)
            #else:
                #addTrackedLayer(self.repo.url, source, dest)         
        self.ui.progressBarImport.setValue(0)
        if not addId:
            QtGui.QMessageBox.information(self, 'Import',
                    "The selected data has been correctly imported.",
                    QtGui.QMessageBox.Ok)
        if config.explorer is not None and config.explorer.currentRepo is not None:
            if config.explorer.currentRepo.url == self.repo.url:
                config.explorer.updateRepoStatusLabelAndToolbar()                
        if self.closeAfterOperation:
            QtGui.QDialog.accept(self)
            self.close()
             
        
    def exportClicked(self):        
        destinationType = self.ui.exportTypeWidget.currentIndex()
        selected = self.ui.layersList.selectedItems()
        if not selected:
            QtGui.QMessageBox.warning(self, 'Export',
                    "No tree has been selected for export.",
                    QtGui.QMessageBox.Ok)   
            return
        path =  selected[0].path     
        if destinationType == self.LAYER:   
            filepath = self.ui.exportFileBox.text().strip()                                                                                                                
            self.repo.exportshp(self.refPanel.getRef().ref, path, filepath)            
        elif destinationType == self.SPATIALITE:
            filepath = self.ui.spatialiteFileBox.text()
            user = self.ui.spatialiteUserBox.text()
            self.repo.exportsl(self.refPanel.getRef().ref, path, filepath, user)
        elif destinationType == self.POSTGIS:
            host = self.ui.pgExportHostBox.text().strip()
            host = "localhost" if host == "" else host
            database = self.ui.pgExportDatabaseBox.text().strip()
            database = "database" if database == "" else database
            user = self.ui.pgExportUserBox.text().strip()
            user = "postgres" if user == "" else user
            password = self.ui.pgExportPasswordBox.text().strip()
            password = "postgres" if password == "" else password
            port = self.ui.pgExportPortBox.text().strip()
            port = "5432" if port == "" else port
            schema = self.ui.pgExportSchemaBox.text().strip()
            schema = "public" if schema == "" else schema            
            table = self.ui.pgExportTableBox.text().strip()
            if table == "":
                QtGui.QMessageBox.warning(self, 'Export',
                    "A destination table must be specified",
                    QtGui.QMessageBox.Ok)
            self.repo.exportpg(self.refPanel.getRef().ref, path, table, database, 
                user, password, schema, host, port)                   
        self.ui.progressBarImport.setValue(0)
        QtGui.QMessageBox.information(self, 'Export',
                    "The selected data has been correctly exported.",
                    QtGui.QMessageBox.Ok)
        if self.ui.openLayerCheckbox.isChecked():
            if destinationType == self.LAYER:   
                layer = QgsVectorLayer(filepath, path, "ogr")                
            elif destinationType == self.SPATIALITE:
                #TODO
                pass
            elif destinationType == self.POSTGIS:
                uri = QgsDataSourceURI()               
                uri.setConnection(host, port, database, user, password)
                uri.setDataSource(schema, table, "the_geom")
                layer = QgsVectorLayer(uri.uri(), path, "postgres")
            QgsMapLayerRegistry.instance().addMapLayers([layer])
            source = os.path.normcase(layer.source())            
            addTrackedLayer(self.repo.url, source, path)                            
    
        QtGui.QDialog.accept(self)
        self.close()
            
    def reject(self):        
        QtGui.QDialog.reject(self)
        self.close()
        
class TreeListItem(QtGui.QListWidgetItem):
    
    layerIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "layer_group.gif"))
    
    def __init__(self, path):
        QtGui.QListWidgetItem.__init__(self, path)
        self.setIcon(self.layerIcon)
        self.path = path
        