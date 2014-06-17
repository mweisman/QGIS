from PyQt4 import QtGui, QtCore
from geogitpy import geogit
from geogitpy.geogitexception import GeoGitException
from geogitpy.py4jconnector import _connect
import subprocess
from geogit.gui.pyqtconnectordecorator import geogitPath
import os
from geogit import config
from py4j.java_gateway import JavaGateway
import logging
import webbrowser

_logger = logging.getLogger("geogitpy")

okIcon = os.path.dirname(__file__) + "/../../ui/resources/ok.png"
notOkIcon = os.path.dirname(__file__) + "/../../ui/resources/notok.gif"
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
        self.textBrowser.connect(self.textBrowser, QtCore.SIGNAL("anchorClicked(const QUrl&)"), self.linkClicked)        
        text = '"<html><img src="' + errorIcon + '"/><h3>Cannot connect to GeoGit.</h3>'
        text += "<p>To connect to GeoGit, you must install GeoGit and have the GeoGit gateway running:</p>"
        text += '<p>Click <a href = "help">here</a> to know more about how to install and run GeoGit</p></html>'        
        self.textBrowser.setHtml(text)        
        layout.addWidget(self.textBrowser)        
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.close)
        
        self.resize(500, 400)
        self.setWindowTitle("Error connecting to GeoGit")
        
    def linkClicked(self):
        webbrowser.open_new_tab("http://ujo.com")  
        self.close()
        