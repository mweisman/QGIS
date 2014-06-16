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

_logger = logging.getLogger("geogitpy")

okIcon = os.path.dirname(__file__) + "/../../ui/resources/ok.png"
notOkIcon = os.path.dirname(__file__) + "/../../ui/resources/notok.gif"
errorIcon = os.path.dirname(__file__) + "/../../ui/resources/error.png"
    
class Py4jCheckDialog(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(Py4jCheckDialog, self).__init__(parent)        
        self.initGui()

        
    def initGui(self):                         
        layout = QtGui.QVBoxLayout()                                
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Close)
        class MyBrowser(QtGui.QTextBrowser):
            def loadResource(self, type_, name):                
                return None        
        self.textBrowser = MyBrowser()
        self.textBrowser.connect(self.textBrowser, QtCore.SIGNAL("anchorClicked(const QUrl&)"), self.linkClicked)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.text = self.checkSetup()
        self.textBrowser.setHtml(self.text)
        QtGui.QApplication.restoreOverrideCursor()
        layout.addWidget(self.textBrowser)        
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"), self.close)
        
        self.resize(500, 400)
        self.setWindowTitle("Error connecting to GeoGit")
        
    def linkClicked(self, url):
        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            _connect()
            QtGui.QMessageBox.warning(self, 'Server correctly started',
                                      "Server is now up and running\n",
                                      QtGui.QMessageBox.Ok)
        except:
            QtGui.QMessageBox.warning(self, 'Cannot start gateway',
                                      "Could not start python gateway and set up a connection",
                                      QtGui.QMessageBox.Ok)
        finally:
            QtGui.QApplication.restoreOverrideCursor()
            self.textBrowser.setHtml(self.text)
        
    def checkSetup(self):
        def _ok(ok):
            icon = okIcon if ok else notOkIcon            
            return'<img src="' + icon + '"/>'
                      
        text = '"<html><img src="' + errorIcon + '"/><p><b>There was a problem connecting to GeoGit.</b></p>'
        text += "<p>The following checks have been performed to find out the reason for this problem:</p>"
        text += "<ul>"
        javaOk, message = self.javaVersion()        
        text += "<li>%s Java: %s </li>" % (_ok(javaOk), message)
        geogitOk, message = self.checkGeoGit()
        text += "<li>%s GeoGit: %s</li>" % (_ok(geogitOk), message)
        ok, message = self.checkPy4J(javaOk and geogitOk)
        text += "<li>%s GeoGit Python connector: %s</li>" % (_ok(ok), message)
        text += "</ul></html>"
        return text
        
    def checkPy4J(self, showConnectOption):
        try: 
            gateway = JavaGateway()       
            gateway.entry_point.isGeoGitServer()  
            return True, "Gateway is up and running"      
        except Exception, e:
            _logger.debug("Error checking gateway:" + e.args[0])
            s = "Gateway is not running"
            if showConnectOption:
                s += '&nbsp;<a href ="start">start gateway</a>'
            return False, s    
        
    def javaVersion(self):        
        try:
            ok, output = self.run(["java", "-version"])                 
            _logger.debug("Output of Java check:" + output)
            if ok:
                version = output.splitlines()[0]
                if "1.7" in version:
                    return True, "%s found" % (version)
                else:
                    return False, "A valid version of Java was not found"
            else:
                return False, "Java not found or cannot be run"
        except:
            return False, "Java not found or cannot be run"
        
    def checkGeoGit(self):      
        try:                
            path = os.path.join(geogitPath, "geogit")        
            if os.path.exists(path): 
                ok, output = self.run([path, "--version"])
                _logger.debug("Output of GeoGit check:" + output)
                if ok:
                    line = output.splitlines()[0].strip()
                    if line.startswith("Project"):
                        return True, "GeoGit %s found" % (line.split(" ")[-1])                
                return False, "GeoGit not found or cannot be executed:<br><ul><li>Output:" + "<br>".join(output.splitlines()) + "</li>"                      
            userPath = config.getConfigValue(config.GENERAL, config.GEOGIT_PATH)
            path = os.path.join(userPath, "geogit")
            if os.path.exists(path): 
                ok, output = self.run([userPath, "--version"])
                _logger.debug("Output of GeoGit check:" + output)
                if ok:
                    line = output.splitlines()[0].strip()
                    if line.startswith("Project"):
                        return True, "GeoGit %s found" % (line.split(" ")[-1]) 
                return False, "GeoGit not found or cannot be executed:<br><ul><li>"+ "<br>".join(output.splitlines()) + "</li>"   
                 
            ok, output = self.run(["geogit", "--version"])
            _logger.debug("Output of GeoGit check:" + output)
            if ok:
                line = output.splitlines()[0].strip()
                if line.startswith("Project"):
                    return True, "GeoGit %s found" % (line.split(" ")[-1])                
            return False, "GeoGit not found or cannot be executed:<br><ul><li>" + "<br>".join(output.splitlines()) + "</li>"                         
        except Exception, e:
            return False, "GeoGit not found or cannot be executed:<br><ul><li>" + "<br>".join(output.splitlines()) + "</li>"   
        
    def run(self, args):
        if os.name != "nt":
            args = " ".join(args)

        try:
            proc = subprocess.Popen(args, shell=os.name == "nt", stdout=subprocess.PIPE, 
                            stdin=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True)
        except Exception, e:
            return False, e.args[0]
        output = []
        for line in iter(proc.stdout.readline, ""):        
            line = line.strip("\n")
            output.append(line)            
        proc.wait()
        returncode = proc.returncode        
        return returncode == 0, "\n".join(output)
        
        