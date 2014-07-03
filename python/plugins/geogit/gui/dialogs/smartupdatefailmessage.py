from PyQt4 import QtGui, QtCore
import os

errorIcon = os.path.dirname(__file__) + "/../../ui/resources/error.png"
    
class SmartUpdateFailMessage(QtGui.QDialog):
    
    def __init__(self, parent, message):
        super(SmartUpdateFailMessage, self).__init__(parent)        
        self.initGui(message)

    def initGui(self, message):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        class MyBrowser(QtGui.QTextBrowser):
            def loadResource(self, type_, name):                
                return None        
        self.textBrowser = MyBrowser()            
        text = ("<p>It was not possible to incorporate the changes in the repository due to the following problem:</p>"
                "<p><b>%s</p></b>" % message
                + "<p>A full import is needed to update the repository.</p>"
                "<p>Click on OK to open the import dialog and import the layer that you have just edited</p>")      
        self.textBrowser.setHtml(text)        
        layout.addWidget(self.textBrowser)        
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"), self.close)
        
        self.resize(500, 300)
        self.setWindowTitle("Cannot perform smart update")        
        