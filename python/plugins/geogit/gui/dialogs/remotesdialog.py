from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RemotesDialog(QtGui.QDialog):
    def __init__(self, parent, repo):        
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.changed = False
        self.repo = repo                
        self.remotes = repo.remotes       
        self.setupUi()        

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle("Remotes manager")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.table = QtGui.QTableWidget()                
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.addRowButton = QtGui.QPushButton()
        self.addRowButton.setText("Add remote")
        self.editRowButton = QtGui.QPushButton()
        self.editRowButton.setText("Edit remote")
        self.removeRowButton = QtGui.QPushButton()
        self.removeRowButton.setText("Remove remote")
        self.buttonBox.addButton(self.addRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.editRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.removeRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.setTableContent()
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.setLayout(self.horizontalLayout)        
        QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.close)
        QObject.connect(self.editRowButton, QtCore.SIGNAL("clicked()"), self.editRow)
        QObject.connect(self.addRowButton, QtCore.SIGNAL("clicked()"), self.addRow)
        QObject.connect(self.removeRowButton, QtCore.SIGNAL("clicked()"), self.removeRow)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.editRowButton.setEnabled(False)
        self.removeRowButton.setEnabled(False)

    def setTableContent(self):
        self.table.clear()
        self.table.setColumnCount(2)        
        self.table.setColumnWidth(0,200)
        self.table.setColumnWidth(1,200)
        self.table.setHorizontalHeaderLabels(["Name", "URL"])        
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.setRowCount(len(self.remotes))                            
        for i, name in enumerate(self.remotes):
            url = self.remotes[name]
            self.table.setRowHeight(i,22)                        
            item = QtGui.QTableWidgetItem(name, 0)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.table.setItem(i,0, item)         
            item = QtGui.QTableWidgetItem(url, 0)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)   
            self.table.setItem(i,1, item)                                                    

        self.table.itemSelectionChanged.connect(self.selectionChanged)
        
    def selectionChanged(self):
        enabled = len(self.table.selectedItems()) > 0
        self.editRowButton.setEnabled(enabled)
        self.removeRowButton.setEnabled(enabled)
        
    def editRow(self):
        item = self.table.item(self.table.currentRow(), 0)
        if item is not None:
            name = item.text() 
            dlg = NewRemoteDialog(name, self)
            dlg.exec_()
            if dlg.name:
                self.repo.removeremote(name)
                self.repo.addremote(dlg.name, dlg.url)
                del self.remotes[name]
                self.remotes[dlg.name] = dlg.url 
                self.setTableContent()
                self.changed = True
            
        

    def removeRow(self):
        item = self.table.item(self.table.currentRow(), 0)
        if item is not None:
            name = item.text()        
            self.repo.removeremote(name)
            del self.remotes[name]
            self.setTableContent()
            self.changed = True

    def addRow(self):
        dlg = NewRemoteDialog(parent = self)
        dlg.exec_()
        if dlg.name:
            self.repo.addremote(dlg.name, dlg.url, None, None)
            self.remotes[dlg.name] = dlg.url 
            self.setTableContent()
            self.changed = True


class NewRemoteDialog(QtGui.QDialog):
    
    def __init__(self, name = None, parent = None):
        super(NewRemoteDialog, self).__init__(parent)
        self.name = None
        self.url = None
        self.initGui()        
        
    def initGui(self):                         
        self.setWindowTitle('New remote')
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)        
                
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        nameLabel = QtGui.QLabel('Name')
        self.nameBox = QtGui.QLineEdit()        
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        layout.addLayout(horizontalLayout)
        
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        urlLabel = QtGui.QLabel('URL')
        self.urlBox = QtGui.QLineEdit()        
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlBox)
        layout.addLayout(horizontalLayout)               
        
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.okPressed)
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.cancelPressed)
        
        self.resize(400,200)            
    
    def okPressed(self):
        self.name = unicode(self.nameBox.text())
        self.url = unicode(self.urlBox.text()) 
        self.close()

    def cancelPressed(self):
        self.name = None
        self.url = None
        self.close()              