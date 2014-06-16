import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsFilterLineEdit
from geogit import config
from geogitpy.py4jconnector import Py4JCLIConnector

   
class ConfigDialog(QDialog):

    repoIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../../ui/resources/repo.gif")
    
    geogitIcon = QtGui.QIcon(os.path.dirname(__file__) + "/../../ui/resources/geogit.png")  

    def __init__(self):
        QDialog.__init__(self)        
        self.setupUi()        
        if hasattr(self.searchBox, 'setPlaceholderText'):
            self.searchBox.setPlaceholderText(self.tr("Search..."))
        self.searchBox.textChanged.connect(self.filterTree)
        self.fillTree()

    def setupUi(self):        
        self.resize(640, 450)
                
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)        
        self.searchBox = QgsFilterLineEdit(self)        
        self.verticalLayout.addWidget(self.searchBox)
        self.tree = QtGui.QTreeWidget(self)
        self.tree.setAlternatingRowColors(True)        
        self.verticalLayout.addWidget(self.tree)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)        
        self.verticalLayout.addWidget(self.buttonBox)
        
        self.setWindowTitle("Configuration options")
        self.searchBox.setToolTip("Enter setting name to filter list")
        self.tree.headerItem().setText(0, "Setting")
        self.tree.headerItem().setText(1, "Value")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.setLayout(self.verticalLayout)                          

    def filterTree(self):
        text = unicode(self.searchBox.text())
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            visible = False
            for j in range(item.childCount()):                                    
                subitem = item.child(j)
                itemText = subitem.text(0)                                        
            if (text.strip() == ""):
                subitem.setHidden(False)
                visible = True
            else:
                hidden = text not in itemText                        
                item.setHidden(hidden)
                visible = visible or not hidden
            item.setHidden(not visible) 
            item.setExpanded(visible and text.strip() != "")
        
    def fillTree(self):
        self.items = {}
        self.tree.clear()
        
        generalItem = self._getItem(config.GENERAL, self.geogitIcon, config.generalParams)        
        self.tree.addTopLevelItem(generalItem)
        geogitConfigItems = self._getGeoGitConfigItems()        
        self.tree.addTopLevelItem(geogitConfigItems)
        self.tree.setColumnWidth(0, 400)

    def _getGeoGitConfigItems(self):
        item = QTreeWidgetItem()
        item.setText(0, "GeoGit settings")        
        item.setIcon(0, self.geogitIcon)
        params = Py4JCLIConnector.getconfigglobal()
        baseParams = ['user.name', 'user.email']
        for baseParam in baseParams:
            if baseParam not in params:
                params[baseParam] = ""
        for paramName, paramValue in params.iteritems():                        
            subItem = TreeGeoGitSettingItem(paramName, paramValue)
            item.addChild(subItem)
        return item
    
    def _getItem(self, name, icon, params):
        item = QTreeWidgetItem()
        item.setText(0, name)        
        item.setIcon(0, icon)
        for param in params:
            paramName, paramDescription, defaultValue = param
            paramName = "/GeoGit/Settings/" + name + "/" + paramName 
            subItem = TreeSettingItem(paramName, paramDescription, defaultValue)
            item.addChild(subItem)
        return item
                    
    def accept(self):
        iterator = QtGui.QTreeWidgetItemIterator(self.tree)
        value = iterator.value()
        while value:            
            if hasattr(value, 'saveValue'):
                value.saveValue()              
            iterator += 1
            value = iterator.value()                    
        QDialog.accept(self)

class TreeGeoGitSettingItem(QTreeWidgetItem):

    def __init__(self, name, value):
        QTreeWidgetItem.__init__(self)
        self.name = name
        self.setText(0, name)   
        self.value = value             
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.setText(1, unicode(value))
            
    def saveValue(self):
        value = self.text(1)
        if value != self.value:        
            Py4JCLIConnector.configglobal(self.name, value)

class TreeSettingItem(QTreeWidgetItem):

    def __init__(self, name, description, defaultValue):
        QTreeWidgetItem.__init__(self)
        self.name = name
        self.setText(0, description)        
        if isinstance(defaultValue,bool):
            self.value = QSettings().value(name, defaultValue=defaultValue, type=bool)            
            if self.value:
                self.setCheckState(1, Qt.Checked)
            else:
                self.setCheckState(1, Qt.Unchecked)
        else:
            self.value = QSettings().value(name, defaultValue=defaultValue)
            self.setFlags(self.flags() | Qt.ItemIsEditable)
            self.setText(1, unicode(self.value))
            
    def saveValue(self):
        if isinstance(self.value,bool):
            self.value = self.checkState(1) == Qt.Checked
        else:
            self.value = self.text(1)
        QSettings().setValue(self.name, self.value)
        
