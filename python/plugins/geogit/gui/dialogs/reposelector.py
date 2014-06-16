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
from geogit.gui.dialogs.userpasswd import UserPasswordDialog
from geogit.tools.ujoconnector import getUjoRepositories,\
    AuthenticationException, createUjoRepository
from geogit import config
from geogit.tools.repodecorator import LocalRepository, InvalidRepoException,\
    wrongRepoIcon
from createujorepodialog import CreateUjoRepoDialog
from requests.exceptions import RequestException
from geogit.gui.executor import execute
import webbrowser
from geogit.tools import ujoconnector


deleteIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "delete.gif"))
cloneIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "clone.png"))
gotoIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "push-repo.png"))
localIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "computer.png"))
ujoIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, os.pardir, "ui", "resources", "ujo-16.png"))

    
class RepoSelectorDialog(QtGui.QDialog):
            
    def __init__(self):
        QtGui.QDialog.__init__(self, config.iface.mainWindow(), 
                               QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint) 
        
        self.repo = None
        self.repoName = None
        
        self.searchLayers = False        
        
        self.localReposItem = None
        self.ujoReposItem = None
        
        self.readLocalReposFromSettings()
                
        self.ui = Ui_RepoSelectorDialog()
        self.ui.setupUi(self)        
        self.ui.addButton.clicked.connect(self.addRepo)
        self.ui.newUjoRepoButton.clicked.connect(self.newUjoRepoButtonClicked)
        self.ui.openOrCloneRepoButton.clicked.connect(self.openOrCloneRepo)                
        self.ui.filterBox.textChanged.connect(self.filterRepos)                        
        self.ui.repoTree.itemClicked.connect(self.treeItemClicked)
        self.ui.advancedSearchButton.clicked.connect(self.advancedSearch)
        self.ui.repoTree.itemDoubleClicked.connect(self.treeItemDoubleClicked)  
        self.connect(self.ui.loggedAsLabel, QtCore.SIGNAL("linkActivated(QString)"), self.loginLinkClicked)
        self.ui.repoTree.customContextMenuRequested.connect(self.showTreePopupMenu)
        self.connect(self.ui.repoDescription, QtCore.SIGNAL("anchorClicked(const QUrl&)"), self.descriptionLinkClicked)
        self.ujoRepos = []
        self.lastSelectedItem = None    
                        
        self.user = None
        self.password = None
        
        self.fillRepoTree()
        self.updateLogLabel()
        
        self.updateCurrentRepo(None)
        
        
    def showTreePopupMenu(self, point):                                    
        items = self.ui.repoTree.selectedItems()
        toDelete = [item for item in items if isinstance(item, RepoItem)]        
        if toDelete:                    
            menu = QtGui.QMenu()
            deleteAction = QtGui.QAction(deleteIcon, "Remove", None)                
            deleteAction.triggered.connect(lambda: self.deleteRepos(toDelete))                
            menu.addAction(deleteAction)
            point = self.ui.repoTree.mapToGlobal(point)                        
            menu.exec_(point)


    def advancedSearch(self):
        def _clicked():
            self.searchLayers = not self.searchLayers
            print self.searchLayers
            self.filterRepos()
        menu = QtGui.QMenu()
        includeLayersAction = QtGui.QAction("Search also in layer names", None)
        includeLayersAction.setCheckable(True)
        includeLayersAction.setChecked(self.searchLayers)                
        includeLayersAction.triggered.connect(_clicked)                
        menu.addAction(includeLayersAction )                                    
        menu.exec_(QtGui.QCursor.pos())
        
        
    def deleteRepos(self, items):
        ujoRepos = False
        localRepos = False
        for item in items:            
            repo = item.repo
            if isinstance(repo, LocalRepository):
                localRepos = True
                self.localReposItem.removeChild(item)
                self.localRepos.remove(repo)
                removeFromRepositoryPool(repo.url)
                for r in self.ujoRepos:
                    if r.localClone == repo.url:
                        r.localClone = None
                        break
            else:
                ujoRepos = True
        
        if localRepos:
            self.saveLocalReposToSettings()    
            self.updateCurrentRepo(None)
        if ujoRepos:
            QtGui.QMessageBox.warning(self, "Cannot remove",
                        "Ujo repositories cannot be removed", 
                        QtGui.QMessageBox.Ok)
    
    def descriptionLinkClicked(self, url):        
        url = url.toString()
        if url == "upload":
            repo = self.newUjoRepo(self.currentRepo.name)
            if repo is not None:            
                self.currentRepo.repo.addremote("ujo", repo.url, self.user, self.password)
                self.currentRepo.repo.push("ujo", all = True)
                self.currentRepo.setUjoData(repo.url, repo.name, repo.title, repo.description)
                repo.localClone = self.currentRepo.url
                self.updateCurrentRepo(self.currentRepo)                
    
      
                
    def loginLinkClicked(self, url):
        if url == "site":                                
            url = ujoconnector.UJO_URL
            webbrowser.open_new_tab(url)            
        elif url == "login":
            dlg = UserPasswordDialog()
            dlg.exec_()
            if dlg.password is not None:
                try:
                    self.loadUjoRepos(dlg.user, dlg.password)
                    self.user = dlg.user
                    self.password = dlg.password
                    self.updateUjoReposItem()
                    self.updateLogLabel()
                except RequestException, e:
                    if "not found" in e.message.lower():
                        QtGui.QMessageBox.warning(self, "Cannot login",
                            "The selected user does not exist\nOpen an account in the Ujo site before using that username", 
                            QtGui.QMessageBox.Ok)
                    else:
                        QtGui.QMessageBox.warning(self, "Cannot login",
                            u"There has been a problem login in:\n" + unicode(e.args[0]), 
                            QtGui.QMessageBox.Ok)
                except AuthenticationException,e: 
                    QtGui.QMessageBox.warning(self, "Wrong credentials",
                        "Wrong user name or password", 
                        QtGui.QMessageBox.Ok)

    def openOrCloneRepo(self):
        if self.currentRepo is None:
            return
        if isinstance(self.currentRepo, LocalRepository): 
            self.repo = self.currentRepo            
            self.close()
        else:
            if self.currentRepo.url in self.ujoClones:
                for repo in self.localRepos:
                    if repo.url == self.ujoClones[self.currentRepo.url]:
                        self.repo = repo            
                        self.close() 
                        return
            cloneDirectly = config.getConfigValue(config.GENERAL, config.CLONE_DIRECTLY)
            path = config.getConfigValue(config.GENERAL, config.CLONE_PARENT_PATH)                         
            if cloneDirectly and os.path.exists(path):
                folder = path
            else:
                folder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Cloned repository folder", path))        
            if folder != "":
                ujoUrl = self.currentRepo.url
                ujoDescription = self.currentRepo.description
                ujoName = self.currentRepo.name
                ujoTitle = self.currentRepo.title
                if self._addRepo(self.currentRepo.url, folder, (ujoUrl, ujoName, ujoTitle, ujoDescription), 
                                 self.user, self.password):
                    self.ujoClones[ujoUrl] = folder                    
                    self.saveLocalReposToSettings()   
                    self.currentRepo.localClone = folder                 
                
    def filterRepos(self):
        text = self.ui.filterBox.text().strip()            
        for i in xrange(self.localReposItem.childCount()):
            item = self.localReposItem.child(i)
            itemText = item.text(0)
            visible = False
            if text == "":
                visible = True
            elif text in itemText:
                visible = True                
            elif self.searchLayers:             
                for layer in item.repo.layers():                    
                    if text in layer:
                        visible = True
                        break            
            item.setHidden(not visible) 
        for i in xrange(self.ujoReposItem.childCount()):
            item = self.ujoReposItem.child(i)
            itemText = item.text(0)            
            item.setHidden(text != "" and text not in itemText)            

    def treeItemClicked(self):    
        if self.ui.repoTree.selectedItems():        
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
        
    @property
    def ujoClones(self):
        ujoClones = {}
        for repo in self.localRepos:
            ujoUrl = repo.ujoUrl
            if ujoUrl is not None:
                ujoClones[ujoUrl] = repo.url   
        return ujoClones                                                         
                            
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

    def _addRepo(self, url, clonePath = None, ujoData = None, user = None, password = None):                                                            
        try:                                                  
            if clonePath is not None:
                if clonePath not in self.localRepos:
                    connector = PyQtConnectorDecorator()
                    connector.checkIsAlive()                                                                                          
                    repo = Repository.newrepofromclone(url, clonePath, connector, user, password)
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
            if ujoData is not None:
                repo.setUjoData(*ujoData)
            self.localRepos.append(repo)
            item = RepoItem(repo)
            self.localReposItem.addChild(item)
            self.localReposItem.setExpanded(True)
            self.ui.repoTree.clearSelection()
            self.lastSelectedItem = item
            self.ui.repoTree.setItemSelected(item, True)
            if self.user is not None:
                self.updateUjoRepos(self.user, self.password)
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
            QtGui.QMessageBox.warning(self, 'Error running geogit',
                "Could not create repository.\n" + str(e), 
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
        self.updateUjoReposItem()
        
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
        

    def updateLogLabel(self):        
        if self.user is not None:
            self.ui.loggedAsLabel.setText("Logged as %s. &nbsp; <a href='login'>Change</a> &nbsp; <a href='site'> Open account page</a>" %(self.user))            
        else:
            self.ui.loggedAsLabel.setText("Not logged. <a href='login'>Log in</a>")
    
    def invalidateRepoDescriptionCache(self):
        for repo in self.localRepos:
            repo.invalidateDescriptionCache()
        
    def updateCurrentRepo(self, repo):               
        if repo is None:
            self.currentRepo = None
            self.ui.repoDescription.setText("")  
            self.ui.repoTree.setCurrentItem(self.localReposItem)  
            self.lastSelectedItem = None  
            self.ui.openOrCloneRepoButton.setEnabled(False)      
        else:
            self.currentRepo = repo
            try:
                desc = repo.fullDescription            
                if isinstance(repo, LocalRepository) or repo.localClone is not None:
                    self.ui.openOrCloneRepoButton.setEnabled(True)
                    self.ui.openOrCloneRepoButton.setIcon(gotoIcon)
                    self.ui.openOrCloneRepoButton.setText("Open repository")
                    if isinstance(repo, LocalRepository) and repo.ujoUrl is None:
                        desc += "<p><b>This repository is not linked to any Ujo repository: &nbsp; <b><a href='upload'>Upload to Ujo</a></p>" 
                else:
                    self.ui.openOrCloneRepoButton.setEnabled(True)
                    self.ui.openOrCloneRepoButton.setIcon(cloneIcon)
                    self.ui.openOrCloneRepoButton.setText("Clone repository")                                                    
            except InvalidRepoException:
                desc = ("<p><b>LOCATION: </b>%s</p><p><b>No repository was found at this location."  % self.currentRepo.url  
                        + "\nIt might have been deleted</b></p>")  
                self.ui.openOrCloneRepoButton.setEnabled(False)
                self.lastSelectedItem.setIcon(0, wrongRepoIcon)

            self.ui.repoDescription.setText(desc)                   


    ########## Ujo############    
    def updateUjoReposItem(self):
        self.ui.repoTree.invisibleRootItem().removeChild(self.ujoReposItem)
        self.ujoReposItem = QtGui.QTreeWidgetItem(["Ujo"])
        self.ujoReposItem.setIcon(0, ujoIcon)
        for repo in self.ujoRepos:
            item = RepoItem(repo)
            self.ujoReposItem.addChild(item)
        self.ui.repoTree.addTopLevelItem(self.ujoReposItem)        
        self.ui.repoTree.sortItems(0, QtCore.Qt.AscendingOrder)
        self.filterRepos()
        self.ujoReposItem.setExpanded(True)

            
    def newUjoRepoButtonClicked(self):
        self.newUjoRepo()
        
    def newUjoRepo(self, name = None):        
        if self.user is None:
            QtGui.QMessageBox.warning(self, "Cannot create Ujo repository",
                        "You have to be logged to create a Ujo repository", 
                        QtGui.QMessageBox.Ok)
            return 
        dlg = CreateUjoRepoDialog(name)
        dlg.exec_()
        if dlg.name is not None:
            try:
                ujoRepo = execute(lambda : createUjoRepository(self.user, self.password, 
                                                               dlg.name, dlg.title, dlg.description))
            except RequestException, e:
                QtGui.QMessageBox.warning(self, "Problem creating repository",
                        "There has been a problem while creating the repository\n" + e.args[0], 
                        QtGui.QMessageBox.Ok)
                return             
            item = RepoItem(ujoRepo)
            self.ujoReposItem.addChild(item)
            self.ujoRepos.append(ujoRepo)
            self.ui.repoTree.sortItems(0, QtCore.Qt.AscendingOrder)
            return ujoRepo
        return 


    def loadUjoRepos(self, user, password):
        self.ujoRepos = execute(lambda : getUjoRepositories(user, password))
        self.updateUjoRepos(user, password)               
    
    def updateUjoRepos(self, user, password):                        
        for repo in self.ujoRepos:
            if repo.url in self.ujoClones:            
                repo.localClone = self.ujoClones[repo.url]
            else:
                repo.localClone = None
            

        
class RepoItem(QtGui.QTreeWidgetItem): 
    def __init__(self, repo): 
        QtGui.QTreeWidgetItem.__init__(self)
        self.repo = repo        
        self.setText(0, repo.title)                
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
    


