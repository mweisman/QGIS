import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from geogit.ui.addlayerdialog import Ui_GeoGitLayerDialog  
from PyQt4 import QtCore, QtGui
from geogit.tools.repodecorator import LocalRepository
from geogit.tools.exporter import exportFromGeoGitToTempFile
from geogitpy import geogit

   
class AddGeoGitLayerDialog(QDialog):
    
    layerIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "ui", "resources", "layer_group.gif"))
            
    def __init__(self, parent = None):
        QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint) 
                        
        self.ui = Ui_GeoGitLayerDialog()
        self.ui.setupUi(self)               
                            
        repos = unicode(QtCore.QSettings().value("/GeoGit/Repos", ""))
        urls = repos.split(";")
        urls= [u for u in urls if u.strip() != ""]
        self.localRepos = [LocalRepository(url) for url in urls]
        for repo in self.localRepos:
            self.ui.repoBox.addItem(repo.name, repo)  
        
        self.ui.connectButton.clicked.connect(self.connectToRepo)
        self.ui.newLocalRepoButton.clicked.connect(self.newLocalRepo)
        self.ui.deleteButton.clicked.connect(self.deleteRepo)
        
        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.okPressed)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.cancelPressed)
                       
    def deleteRepo(self): 
        if self.ui.repoBox.count() == 0:
            return                   
        repo = self.ui.repoBox.itemData(self.ui.repoBox.currentIndex())        
        self.localRepos.remove(repo)        
        self.ui.repoBox.removeItem(self.ui.repoBox.currentIndex())
        value = ";".join([r.url for r in self.localRepos])
        QtCore.QSettings().setValue("/GeoGit/Repos", value)
        self.ui.layersList.clear()
        
    def connectToRepo(self):
        repo = self.ui.repoBox.itemData(self.ui.repoBox.currentIndex())
        if repo is None:
            return
        self.repo = repo.repo        
        trees = self.repo.head.root.trees
        self.ui.layersList.clear()
        for tree in trees:
            item = QtGui.QListWidgetItem(tree.path)
            item.setIcon(self.layerIcon)  
            self.ui.layersList.addItem(item)          
        
    def newLocalRepo(self):            
        settings = QtCore.QSettings()        
        path = settings.value("/GeoGit/LastAddedRepo", "") 
        folder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "GeoGit repository folder", path))       
        if folder != "":            
            repo = LocalRepository(folder)
            self.localRepos.append(repo)
            self.ui.repoBox.addItem(repo.name, repo)
            self.ui.repoBox.setCurrentIndex(self.ui.repoBox.count() - 1)
    
    def okPressed(self):        
        selected = self.ui.layersList.selectedItems()
        if not selected:
            QtGui.QMessageBox.warning(self, 'Export',
                    "No tree has been selected for export.",
                    QtGui.QMessageBox.Ok)   
            return
        path =  selected[0].text()
        exportFromGeoGitToTempFile(self.repo, geogit.HEAD, path)           
        self.close()
        
    def cancelPressed(self):
        self.close()

