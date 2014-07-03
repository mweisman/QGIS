from PyQt4 import QtGui, QtCore
import os
import logging

_logger = logging.getLogger("geogitpy")

errorIcon = os.path.dirname(__file__) + "/../../ui/resources/error.png"
    
class GatewayNotAvailableDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(GatewayNotAvailableDialog, self).__init__(parent)        
        self.initGui()

        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Close)
        class MyBrowser(QtGui.QTextBrowser):
            def loadResource(self, type_, name):                
                return None        
        self.textBrowser = MyBrowser()    
        text = '"<html><img src="' + errorIcon + '"/><h3>Cannot connect to GeoGit.</h3>'
        text += "<p>To connect to GeoGit, you must install GeoGit and have the GeoGit gateway running:</p>"     
        self.textBrowser.setHtml(text)        
        layout.addWidget(self.textBrowser)        
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.close)
        
        self.resize(500, 400)
        self.setWindowTitle("Error connecting to GeoGit")
