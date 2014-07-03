from PyQt4 import QtGui
from geogit.gui.dialogs.geogitref import RefWidget


class CreateBranchDialog(QtGui.QDialog):
    
    def __init__(self, repo, ref = None, parent = None):
        super(CreateBranchDialog, self).__init__(parent)
        self.ok = False
        self.repo = repo
        self.ref = ref
        self.initGui()
        
        
    def initGui(self):             
        self.setWindowTitle("Create branch")            
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)
        self.refwidget = RefWidget(self.repo)
        self.refwidget.setref(self.ref)
        
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Branch name')
        self.nameBox = QtGui.QLineEdit()
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        
        horizontalLayout2 = QtGui.QHBoxLayout()
        horizontalLayout2.setSpacing(30)
        horizontalLayout2.setMargin(20)        
        self.forceCheck = QtGui.QCheckBox('Force')        
        horizontalLayout2.addWidget(self.forceCheck)
        self.checkoutCheck = QtGui.QCheckBox('Checkout')
        horizontalLayout2.addWidget(self.checkoutCheck)
        
        layout.addLayout(horizontalLayout)
        layout.addWidget(self.refwidget)
        layout.addLayout(horizontalLayout2)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(400,300)
        
    def getRef(self):
        return self.ref
    
    def getName(self):
        return str(self.nameBox.text())
    
    def isForce(self):
        return self.force
    
    def isCheckout(self):
        return self.checkout
          
    def okPressed(self):
        self.ref = self.refwidget.getref()
        self.force = self.forceCheck.isChecked()
        self.checkout = self.checkoutCheck.isChecked()
        self.ok = True
        self.close()

    def cancelPressed(self):
        self.ok = False
        self.close()  