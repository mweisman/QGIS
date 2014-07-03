from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from geogit import config
from geogitpy.py4jconnector import Py4JConnectionException
from geogitpy.geogitexception import GeoGitException

class GeoGitThread(QThread):
    
    finished = pyqtSignal()
            
    def __init__(self, func):
        QThread.__init__(self)       
        self.func = func 
        self.returnValue = [] 
        self.exception = None     
                                                                    
    def run (self):                
        try:
            self.returnValue = self.func()            
            self.finished.emit()
        except Exception, e:                      
            self.exception = e
            self.finished.emit()

_dialog = None

def execute(func, message = None):
    global _dialog
    cursor = QApplication.overrideCursor()    
    waitCursor = (cursor is not None and cursor.shape() == Qt.WaitCursor)
    dialogCreated = False
    try:
        QCoreApplication.processEvents()
        if not waitCursor:                     
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))                                               
               
        if message is not None:
            t = GeoGitThread(func)            
            loop = QEventLoop()            
            t.finished.connect(loop.exit, Qt.QueuedConnection) 
            if _dialog is None: 
                dialogCreated = True
                _dialog = QProgressDialog(message, None, 0, 0  , config.iface.mainWindow())
                _dialog.setWindowModality(Qt.WindowModal);
                _dialog.setMinimumDuration(1)  
                _dialog.showNormal()
            else:                
                oldText = _dialog.labelText()
                _dialog.setLabelText(message)
            QApplication.processEvents()  
            t.start()            
            loop.exec_(flags=QEventLoop.ExcludeUserInputEvents)
            if t.exception is not None:                    
                raise t.exception      
            return t.returnValue   
        else:
            return func()                         
    finally:    
        if message is not None: 
            if dialogCreated:                       
                _dialog.hide()
                _dialog = None
            else:
                _dialog.setLabelText(oldText)
        if not waitCursor:
            QApplication.restoreOverrideCursor() 
        QCoreApplication.processEvents()
