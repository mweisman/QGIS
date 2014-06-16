import os
from PyQt4 import QtGui, QtCore
from qgis.core import *
from geogit.ui.addrepodialog import Ui_AddRepoDialog
from geogitpy.py4jconnector import Py4JCLIConnector
from geogitpy.geogitexception import GeoGitException
from geogitpy.geogitserverconnector import GeoGitServerConnector
from geogitpy.repo import isremoteurl
from requests.exceptions import RequestException
from geogit.gui.executor import execute


class AddRepoDialog(QtGui.QDialog):
    
    ADD = 0
    CREATE = 1
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)                    
        self.ui = Ui_AddRepoDialog()
        self.ui.setupUi(self)
        self.ui.cloneCheckBox.stateChanged.connect(self.cloneCheckChanged)
        self.ui.selectCloneFolderButton.clicked.connect(self.selectCloneFolder)
        self.ui.selectRepoFolderButton.clicked.connect(self.selectRepoFolder)
        self.ui.selectNewRepoFolderButton.clicked.connect(self.selectNewRepoFolder)
        self.ui.addRepoButton.clicked.connect(self.addRepo)
        self.ui.createRepoButton.clicked.connect(self.createRepo)
        self.ui.createRepoAndImportButton.clicked.connect(self.createRepoAndImport)
        self.ui.cloneFolderBox.textChanged.connect(self.updateAddRepoButton)
        self.ui.addRepoFolderBox.textChanged.connect(self.updateAddRepoButton)
        self.ui.createRepoFolderBox.textChanged.connect(self.updateCreateRepoButtons)                
        self.ui.createRepoButton.setEnabled(False)
        self.ui.createRepoAndImportButton.setEnabled(False)     
        self.updateAddRepoButton()        
        self.ok = False 
        
        
    def updateAddRepoButton(self):
        enabled = self.ui.addRepoFolderBox.text().strip() != ""
        if self.ui.cloneCheckBox.isChecked():
            enabled = enabled and self.ui.cloneFolderBox.text().strip() != ""
        self.ui.addRepoButton.setEnabled(enabled)    

    def updateCreateRepoButtons(self):
        enabled = self.ui.createRepoFolderBox.text().strip() != ""        
        self.ui.createRepoButton.setEnabled(enabled)
        self.ui.createRepoAndImportButton.setEnabled(enabled)        
    
    def cloneCheckChanged(self):
        self.updateAddRepoButton()       
      
    def selectRepoFolder(self):
        settings = QtCore.QSettings()        
        path = settings.value("/GeoGit/LastAddedRepo", "") 
        folder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "GeoGit repository folder", path))       
        if folder != "":            
            self.ui.addRepoFolderBox.setText(folder)
                    
    def selectCloneFolder(self):
        folder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "GeoGit repository folder"))        
        if folder != "":
            self.ui.cloneFolderBox.setText(folder)
            
    def selectNewRepoFolder(self):
        folder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "GeoGit repository folder"))        
        if folder != "":
            self.ui.createRepoFolderBox.setText(folder)            
        
   
    def addRepo(self):
        self.ok = True
        self.mode = self.ADD
        self.path = self.ui.addRepoFolderBox.text().strip()
        if self.ui.cloneCheckBox.isChecked():
            self.clonePath = self.ui.cloneFolderBox.text()
        else:
            if isremoteurl(self.path):
                QtGui.QMessageBox.warning(self, "Remote repositories not supported",
                        "Direct connection to a remote repository is not supported\n"
                        "Select the 'Clone repo' check box to clone it locally", 
                        QtGui.QMessageBox.Ok)
                self.path = None
                self.ok = False
                return
            self.clonePath = None
        settings = QtCore.QSettings()
        settings.setValue("/GeoGit/LastAddedRepo", self.path)            
        self.close()
            
    def createRepo(self):        
        self.mode = self.CREATE
        self.path = self.ui.createRepoFolderBox.text()
        if isremoteurl(self.path):
            name = os.path.basename(self.path)
            url = os.path.dirname(self.path)
            try:
                execute(lambda : GeoGitServerConnector.createrepo(url, name))
            except RequestException, e:
                    QtGui.QMessageBox.warning(self, "Cannot create repository",
                        "There has been a problem creating the remote repository:\n" + e.args[0], 
                        QtGui.QMessageBox.Ok)
                    return
            ok = QtGui.QMessageBox.warning(self, "Create remote repository",
                    "The remote repository has been created\n"
                    "To be able to connect to it, you must clone it locally\n"
                    "Do you want to clone it now?", 
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)                        
            if ok == QtGui.QMessageBox.Yes:
                self.ui.addRepoFolderBox.setText(self.path)
                self.ui.cloneCheckBox.setChecked(True)
                return
            self.ok = False
        self.ok = True
        self.importData = False
        self.close()
        
    def createRepoAndImport(self):
        self.ok = True
        self.mode = self.CREATE
        self.path = self.ui.createRepoFolderBox.text()
        self.importData = True
        self.close()   
   
    
    def reject(self):        
        QtGui.QDialog.reject(self)