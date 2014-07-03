from PyQt4 import QtGui, QtCore
from geogitpy import geogit
from geogitpy.geogitexception import GeoGitException
from geogitref import RefDialog, RefWidget


class CheckoutDialog(RefDialog):
    
    def __init__(self, repo, parent = None):
        super(RefDialog, self).__init__(parent)
        self.repo = repo
        self.ref = None
        self.branchName = None
        self.initGui()

        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)
        self.refwidget = RefWidget(self.repo)
        layout.addWidget(self.refwidget)        
        self.createBranchCheck = QtGui.QCheckBox("Create branch")        
        self.createBranchCheck.stateChanged.connect(self.stateChanged)
        self.branchNameLabel = QtGui.QLabel("Branch name")        
        self.branchNameBox = QtGui.QLineEdit()        
        self.branchNameBox.setEnabled(False)
        layout.addWidget(self.createBranchCheck)                        
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(self.branchNameLabel)
        hlayout.addWidget(self.branchNameBox)
        layout.addLayout(hlayout)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,180)
        self.setWindowTitle("Reference")
               
    def stateChanged(self):
        self.branchNameBox.setEnabled(self.createBranchCheck.isChecked())
        
    def okPressed(self):
        if self.createBranchCheck.isChecked():
            branchName = self.branchNameBox.text()
            if branchName.strip() == "":
                self.branchNameBox.setStyleSheet("QLineEdit{background: yellow}")
                return
            else:
                self.branchNameBox.setStyleSheet("QLineEdit{background: white}")
                self.branchName = branchName
        else:
            self.branchName = None
        try:
            self.ref = self.refwidget.getref()
        except GeoGitException, e:
            self.branchName = None
            QtGui.QMessageBox.warning(self, 'Wrong reference',
                        str(e),
                        QtGui.QMessageBox.Ok)
            return
        self.close()

    def cancelPressed(self):
        self.ref = None
        self.branchName = None
        self.close()