from PyQt4 import QtGui

class UserPasswordDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(UserPasswordDialog, self).__init__(parent)
        self.user = None
        self.password = None
        self.initGui()        
        
    def initGui(self):                         
        self.setWindowTitle('Credentials')
        verticalLayout = QtGui.QVBoxLayout()                                            
                
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        usernameLabel = QtGui.QLabel('User name')
        self.usernameBox = QtGui.QLineEdit()        
        horizontalLayout.addWidget(usernameLabel)
        horizontalLayout.addWidget(self.usernameBox)
        verticalLayout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        passwordLabel = QtGui.QLabel('Password')
        self.passwordBox = QtGui.QLineEdit()   
        self.passwordBox.setEchoMode(QtGui.QLineEdit.Password)       
        horizontalLayout.addWidget(passwordLabel)
        horizontalLayout.addWidget(self.passwordBox)
        verticalLayout.addLayout(horizontalLayout)
               
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setTitle("user/password")
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
        self.password = unicode(self.passwordBox.text()) 
        self.close()

    def cancelPressed(self):
        self.user = None
        self.password = None
        self.close()  
        