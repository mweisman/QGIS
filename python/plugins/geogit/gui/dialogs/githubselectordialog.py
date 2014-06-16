from PyQt4.QtCore import *
from PyQt4.QtGui import *
from geogit.ui.githubselectordialog import Ui_GitHubSelectorDialog  
from geogit.tools.githubimporter import GitHubConnectionException,\
    getGitHubRepos

    
class GitHubSelectorDialog(QDialog):
            
    def __init__(self, parent = None):
        QDialog.__init__(self, parent) 
        
        self.user = None
        self.password = None                
        self.path = None
        self.name = None
                        
        self.ui = Ui_GitHubSelectorDialog()
        self.ui.setupUi(self)        
        self.ui.fetchReposButton.clicked.connect(self.fetchRepos)
        self.ui.selectRepoFolderButton.clicked.connect(self.selectRepoFolder)
        
        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.okPressed)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.cancelPressed)
        
    def selectRepoFolder(self):
        folder = unicode(QFileDialog.getExistingDirectory(self, "GeoGit repository folder"))        
        if folder != "":
            self.ui.repoFolderBox.setText(folder)
                    
    def fetchRepos(self):       
        try:            
            user = self._checkField(self.ui.userBox)            
            password = self._checkField(self.ui.passwordBox)
            owner = self.ui.ownerBox.text()
            if owner.strip() == "":
                owner = user
        except:
            return        
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor)) 
            repos = getGitHubRepos(user, password, owner)            
            self.ui.nameBox.clear()
            for repo in repos:
                self.ui.nameBox.addItem(repo["name"])
                QApplication.restoreOverrideCursor()     
        except GitHubConnectionException, e:
            QApplication.restoreOverrideCursor()              
            QMessageBox.warning(self, "Could not fetch repositories", e.args[0],
                    QMessageBox.Ok)
        
    
    def _checkField(self, widget):
        widget.setStyleSheet("QLineEdit{background: white}")
        text = widget.text()
        if text.strip() == "":
            widget.setStyleSheet("QLineEdit{background: yellow}")
            raise Exception("Wrong value")
        else:
            return text
        
    def okPressed(self):
        try:
            self.user = self._checkField(self.ui.userBox)
            self.path = self._checkField(self.ui.repoFolderBox)
            self.name = self._checkField(self.ui.nameBox.lineEdit())
            self.password = self._checkField(self.ui.passwordBox)
            self.owner = self.ui.ownerBox.text()
            if self.owner.strip() == "":
                self.owner = self.user
            self.close()
        except Exception, e:
            self.user = None
            self.password = None                
            self.path = None
            self.name = None            
        
    def cancelPressed(self):
        self.close()
    