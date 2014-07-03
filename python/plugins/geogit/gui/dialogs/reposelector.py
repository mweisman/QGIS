import os
from PyQt4 import QtGui, QtCore
from qgis.core import *
from geogit.ui.reposelector import Ui_RepoSelectorDialog 
from geogitpy.py4jconnector import Py4JCLIConnector
from geogitpy.repo import Repository
from geogitpy.geogitexception import GeoGitException
from geogit.gui.dialogs.addrepodialog import AddRepoDialog 
from geogit.gui.pyqtconnectordecorator import createRepository,\
    PyQtConnectorDecorator, removeFromRepositoryPool
from geogit.gui.dialogs.importexportdialog import ImportExportDialog
from py4j.protocol import Py4JJavaError
from geogit import config
from geogit.tools.repodecorator import LocalRepository, InvalidRepoException,\
    wrongRepoIcon, repoIcon


deleteIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "delete.gif"))
cloneIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "clone.png"))
gotoIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "push-repo.png"))
localIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "computer.png"))

    
class RepoSelectorDialog(QtGui.QDialog):
            
    def __init__(self):
        QtGui.QDialog.__init__(self, config.iface.mainWindow(), 
                               QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint) 
        
        self.repo = None
        self.repoName = None        
        
        self.localReposItem = None

        self.readLocalReposFromSettings()
                
        self.ui = Ui_RepoSelectorDialog()
        self.ui.setupUi(self)        
        self.ui.addButton.clicked.connect(self.addRepo)        
        self.ui.openOrCloneRepoButton.clicked.connect(self.openOrCloneRepo)                
        self.ui.filterBox.textChanged.connect(self.filterRepos)                        
        self.ui.repoTree.itemClicked.connect(self.treeItemClicked)
        self.ui.repoTree.itemDoubleClicked.connect(self.treeItemDoubleClicked)  
        self.ui.repoTree.customContextMenuRequested.connect(self.showTreePopupMenu)             
        self.lastSelectedItem = None    
                        
        self.user = None
        self.password = None
        
        self.fillRepoTree()
        self.updateCurrentRepo(None)
        
        
    def showTreePopupMenu(self, point):                                    
        items = self.ui.repoTree.selectedItems()
        toDelete = [item for item in items if isinstance(item, RepoItem)]        
        if toDelete:                    
            menu = QtGui.QMenu()
            deleteAction = QtGui.QAction(deleteIcon, "Remove", None)                
            deleteAction.triggered.connect(lambda: self.deleteLocalRepos(toDelete))                
            menu.addAction(deleteAction)
            point = self.ui.repoTree.mapToGlobal(point)                        
            menu.exec_(point)

    def deleteLocalRepos(self, items):
        for item in items:
            repo = item.repo
            self.localReposItem.removeChild(item)
            self.localRepos.remove(repo)
            removeFromRepositoryPool(repo.repo.url)       
        self.saveLocalReposToSettings()
        self.updateCurrentRepo(None)

    def openOrCloneRepo(self):
        if self.currentRepo is None:
            return
        if isinstance(self.currentRepo, LocalRepository): 
            self.repo = self.currentRepo            
            self.close()        
            
    def filterRepos(self):
        text = self.ui.filterBox.text().strip()            
        for i in xrange(self.localReposItem.childCount()):
            item = self.localReposItem.child(i)
            itemText = item.text(0)            
            item.setHidden(text != "" and text not in itemText)            

    def treeItemClicked(self):                          
        item = self.ui.repoTree.selectedItems()[0]
        if self.lastSelectedItem == item:
            return
        self.lastSelectedItem = item
        if isinstance(item, RepoItem):
            self.updateCurrentRepo(item.repo)
        else:
            self.updateCurrentRepo(None)

    def treeItemDoubleClicked(self):                          
        item = self.ui.repoTree.selectedItems()[0]               
        if isinstance(item, RepoItem):
            if isinstance(item.repo, LocalRepository): 
                self.repo = item.repo            
                self.close()            
            
            
    def saveLocalReposToSettings(self):
        value = ";".join([r.url for r in self.localRepos])
        QtCore.QSettings().setValue("/GeoGit/Repos", value)
        
    def readLocalReposFromSettings(self): 
        repos = unicode(QtCore.QSettings().value("/GeoGit/Repos", ""))
        if repos.startswith("NULL"): 
            repos = ""
        urls = repos.split(";")
        urls= [u for u in urls if u.strip() != ""]
        self.localRepos = [LocalRepository(url) for url in urls]      
                                
                            
    def addRepo(self):
        dlg = AddRepoDialog(self)
        dlg.exec_() 
        if dlg.ok:
            if dlg.mode == AddRepoDialog.ADD:
                self._addRepo(dlg.path, dlg.clonePath)
            else:
                created = self.createRepo(dlg.path)
                if dlg.importData and created:
                    dlg = ImportExportDialog(self, self.currentRepo.repo, ImportExportDialog.IMPORT)
                    dlg.exec_()                      
            self.saveLocalReposToSettings()

    def _addRepo(self, url, clonePath = None):                                                            
        try:                                                  
            if clonePath is not None:
                if clonePath not in self.localRepos:
                    connector = PyQtConnectorDecorator()
                    connector.checkIsAlive()                                                                                          
                    repo = Repository.newrepofromclone(url, clonePath, connector)
                else:
                    QtGui.QMessageBox.warning(self, 'Repository already exist',
                                          "The selected clone folder already contains\na repository being tracked", 
                                          QtGui.QMessageBox.Ok)
                    return False                                   
                url = clonePath  
            repos = [r.url for r in self.localRepos]                    
            if url in repos:
                QtGui.QMessageBox.warning(self, 'Repository already exist',
                                          "The selected repository is already tracked", 
                                          QtGui.QMessageBox.Ok)  
                return False               
            createRepository(url, False)                                                 
            repo = LocalRepository(url)
            self.localRepos.append(repo)
            item = RepoItem(repo)            
            self.localReposItem.addChild(item)
            self.localReposItem.setExpanded(True)
            self.ui.repoTree.clearSelection()
            self.ui.repoTree.setItemSelected(item, True)
            self.lastSelectedItem = item
            self.updateCurrentRepo(repo)
            return True                                                                                                                        
        except GeoGitException, e:            
            QtGui.QMessageBox.warning(self, 'Could not add repository',
                                          str(e), 
                                          QtGui.QMessageBox.Ok)
            return False                                        
        except Py4JJavaError, e:            
            QtGui.QMessageBox.warning(self, 'Error running geogit',
                                          "Could not add repository.\nCheck that the specified paths are correct.",
                                          QtGui.QMessageBox.Ok)
            return False            
    
            
    def createRepo(self, path):                                
        try:                                            
            createRepository(path, True)                        
            repo = LocalRepository(path)
            self.localRepos.append(repo)
            item = RepoItem(repo)
            self.localReposItem.addChild(item)
            self.localReposItem.setExpanded(True)
            self.ui.repoTree.clearSelection()
            self.ui.repoTree.setItemSelected(item, True)
            self.lastSelectedItem = item
            self.updateCurrentRepo(repo)   
            return True                                               
        except GeoGitException, e:                
            QtGui.QMessageBox.warning(self, 'Could not create repository',
                                      str(e),                                     
                                      QtGui.QMessageBox.Ok)
            return False
        except Py4JJavaError, e:
            QtGui.QMessageBox.warning(self, 'Error running geogit',
                "Could not create repository.\nCheck that the specified paths are correct.",
                QtGui.QMessageBox.Ok)
            return False       
        
    def fillRepoTree(self):
        self.ui.repoTree.clear() 
        self.updateLocalRepos()
        
    def updateLocalRepos(self):       
        self.ui.repoTree.invisibleRootItem().removeChild(self.localReposItem)
        self.localReposItem = QtGui.QTreeWidgetItem(["Local"])
        self.localReposItem.setIcon(0, localIcon)  
        self.ui.repoTree.insertTopLevelItem(0, self.localReposItem)
        for repo in self.localRepos:            
            item = RepoItem(repo)
            self.localReposItem.addChild(item)        
        self.ui.repoTree.sortItems(0, QtCore.Qt.AscendingOrder)
        self.localReposItem.setExpanded(True)

    
    def invalidateRepoDescriptionCache(self):
        for repo in self.localRepos:
            repo.invalidateDescriptionCache()
        
    def updateCurrentRepo(self, repo): 
        self.currentRepo = repo              
        if repo is None:            
            self.ui.repoDescription.setText("")  
            self.ui.repoTree.setCurrentItem(self.localReposItem)  
            self.lastSelectedItem = None  
            self.ui.openOrCloneRepoButton.setEnabled(False)      
        else:
            try:
                desc = repo.fullDescription
                self.ui.openOrCloneRepoButton.setEnabled(True)
                self.ui.openOrCloneRepoButton.setIcon(gotoIcon)
                self.ui.openOrCloneRepoButton.setText("Open repository") 
                if self.lastSelectedItem is not None:
                    self.lastSelectedItem.setIcon(0, repoIcon)               
            except InvalidRepoException:
                desc = ("<p><b>LOCATION: </b>%s</p><p><b>No repository was found at this location."  % self.currentRepo.url  
                    + "\nIt might have been deleted</b></p>")  
                self.ui.openOrCloneRepoButton.setEnabled(False)
                self.lastSelectedItem.setIcon(0, wrongRepoIcon)

            self.ui.repoDescription.setText(desc)                   

            

        
class RepoItem(QtGui.QTreeWidgetItem): 
    def __init__(self, repo): 
        QtGui.QTreeWidgetItem.__init__(self)
        self.repo = repo        
        self.setText(0, repo.name)                
        self.setIcon(0, repo.icon)          


_repoSelectorDialog = None
def getRepo():
    global _repoSelectorDialog
    if _repoSelectorDialog is None:
        _repoSelectorDialog = RepoSelectorDialog()
    _repoSelectorDialog.invalidateRepoDescriptionCache()
    _repoSelectorDialog.updateCurrentRepo(None)
    _repoSelectorDialog.repo = None
    _repoSelectorDialog.exec_()
    return _repoSelectorDialog.repo
    


