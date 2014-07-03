from PyQt4 import QtGui, QtCore


class DefineRemoteRepoDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(DefineRemoteRepoDialog, self).__init__(parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.url = None
        self.password = None
        self.user = None
        self.name = None
        self.ok = False
        self.initGui()
        
        
    def initGui(self):                         
        self.setWindowTitle('Remote repository definition')
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
        
        repoLayout = QtGui.QVBoxLayout()     
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Repository name')
        self.nameBox = QtGui.QLineEdit()
        self.nameBox.setText('Remote repository')
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        repoLayout.addLayout(horizontalLayout)
                
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        urlLabel = QtGui.QLabel('URL')
        self.urlBox = QtGui.QLineEdit()        
        url = QtCore.QSettings().value('/OpenGeo/LastRemoteRepoUrl', '')                    
        self.urlBox.setText(url)
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlBox)
        repoLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        folderLabel = QtGui.QLabel('Repository folder')
        self.folderBox = FolderSelectionPanel()
        folder = QtCore.QSettings().value('/OpenGeo/LastRepoFolder', '') 
        self.folderBox.text.setText(folder)       
        horizontalLayout.addWidget(folderLabel)
        horizontalLayout.addWidget(self.folderBox)
        repoLayout.addLayout(horizontalLayout)
        
        groupRepo = QtGui.QGroupBox("Repostories")
        groupRepo.setLayout(repoLayout)
 
        credentialsLayout = QtGui.QVBoxLayout()        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QtGui.QLabel('User name')
        self.usernameBox = QtGui.QLineEdit()
        self.usernameBox.setText('admin')
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        credentialsLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QtGui.QLabel('Password')
        self.passwordBox = QtGui.QLineEdit()
        self.passwordBox.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.passwordBox.setText('')
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        credentialsLayout.addLayout(horizontalLayout)
        
        groupCredentials = QtGui.QGroupBox("Credentials")
        groupCredentials.setLayout(credentialsLayout)
        
        layout.addWidget(groupRepo)
        layout.addWidget(groupCredentials)               
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200)
            

    def okPressed(self):        
        self.url = unicode(self.urlBox.text())
        self.name = unicode(self.nameBox.text())
        self.folder = self.folderBox.text.text()
        settings = QtCore.QSettings()
        settings.setValue('/OpenGeo/LastRemoteRepoUrl', self.urlBox.text())
        settings.setValue('/OpenGeo/LastRemotefolder', self.folderBox.text.text())
        self.ok = True        
        self.close()

    def cancelPressed(self):
        self.ok = False
        self.close()  

class FolderSelectionPanel(QtGui.QWidget):

    def __init__(self):
        super(FolderSelectionPanel, self).__init__(None)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.text = QtGui.QLineEdit()        
        self.text.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.horizontalLayout.addWidget(self.text)
        self.pushButton = QtGui.QPushButton()
        self.pushButton.setText("...")
        self.pushButton.clicked.connect(self.buttonPushed)
        self.horizontalLayout.addWidget(self.pushButton)
        self.setLayout(self.horizontalLayout)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

    def buttonPushed(self):
        folder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "GeoGit repository folder"));
        if folder != "":         
            self.text.setText(folder)        

   
        