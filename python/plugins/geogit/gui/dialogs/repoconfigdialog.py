from PyQt4 import QtGui

class RepoConfigDialog(QtGui.QDialog):
    
    def __init__(self, repo, parent = None):
        super(RepoConfigDialog, self).__init__(parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.user = None
        self.email = None
        self.repo = repo
        self.initGui()        
        
    def initGui(self):                         
        self.setWindowTitle('Repository configuration')
        verticalLayout = QtGui.QVBoxLayout()                                            
                
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QtGui.QLabel('User name')
        self.usernameBox = QtGui.QLineEdit()
        value = self.repo.getconfig("user.name")
        if value is not None:
            self.usernameBox.setText(value)        
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        emailLabel = QtGui.QLabel('User email')
        self.emailBox = QtGui.QLineEdit()
        value = self.repo.getconfig("user.email")
        if value is not None:  
            self.emailBox.setText(value)          
        horizontalLayout.addWidget(emailLabel)
        horizontalLayout.addWidget(self.emailBox)
        verticalLayout.addLayout(horizontalLayout)
               
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("User data")
        self.groupBox.setLayout(verticalLayout)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox) 
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)
          
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,200)
            
    
    def okPressed(self):
        self.user = unicode(self.usernameBox.text())
        self.email = unicode(self.emailBox.text()) 
        self.close()

    def cancelPressed(self):
        self.user = None
        self.email = None
        self.close()  