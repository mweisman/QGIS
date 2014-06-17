import os
import signal
import logging
import subprocess
import time
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from geogitpy.py4jconnector import (Py4JCLIConnector, setGatewayPort, _runGateway, 
                            removeProgressListener, Py4JConnectionException, setProgressListener)
from geogitpy.geogitexception import GeoGitException
from geogitpy.repo import Repository
from geogit import config
from geogit.gui.executor import execute
from py4j.java_gateway import JavaGateway, GatewayClient
from py4j.protocol import Py4JNetworkError

_logger = logging.getLogger("geogitpy")
   
def geogitPath():            
    if sys.platform == 'darwin':
        return os.path.join(QgsApplication.prefixPath(), 'bin', 'geogit' 'bin')            
    else:
        return os.path.join(os.path.dirname(QgsApplication.prefixPath()), 'geogit', 'bin')                            

def geogitVersion():
    try:
        from geogitpy.py4jconnector import geogitVersion as _geogitVersion
        return execute(_geogitVersion)            
    except:         
        return "Cannot resolve geogit version. Geogitpy version is too old" 
    
    
class PyQtConnectorDecorator(Py4JCLIConnector):
    
    progressMessages = {"rev-list": "Retrieving repository history",
                            "commit" : "Committing",                             
                            "shp import" : "Importing shapefile",
                            "shp export" : "Exporting shapefile",
                            "pg import" : "Importing from PostGIS database",
                            "pg export" : "Exporting to PostGIS database",
                            "sl import" : "Importing from SpatialLite database",
                            "sl export" : "Exporting to SpatialLite database",
                            "add": "Adding features to repository",
                            "push": "Pushing to remote repository",
                            "pull": "Pulling from remote repository"}
       
    def _getProgressMessage(self, commands):
        if commands[0] == "rev-list" and "-n" in commands:
            #log listing is long only if getting full log.
            return None
        s = " ".join(commands)
        for cmd, msg in self.progressMessages.iteritems():
            if s.startswith(cmd):
                return msg 
        
    def run(self, commands): 
        try:
            return self.runDecorated(lambda: Py4JCLIConnector.run(self, commands), self._getProgressMessage(commands))
        except Py4JConnectionException:            
            startGateway()                        
            return self.runDecorated(lambda: Py4JCLIConnector.run(self, commands), self._getProgressMessage(commands))
        
    def runDecorated(self, func, progressMessage = None):                       
        port = config.getConfigValue(config.GENERAL, config.GATEWAY_PORT)
        setGatewayPort(port)
        return execute(func, progressMessage)        
    
    def checkIsAlive(self): 
        try:
            self.runDecorated(lambda: Py4JCLIConnector.checkIsAlive(self))    
        except Py4JConnectionException:            
            startGateway()                        
            self.runDecorated(lambda: Py4JCLIConnector.checkIsAlive(self))    
            
                                           
    @staticmethod 
    def clone(url, dest, username = None, password = None):        
        commands = ['clone', url, dest]
        if username is not None and password is not None:
            commands.extend(["--username", username, "--password", password])                    
        port = config.getConfigValue(config.GENERAL, config.GATEWAY_PORT)
        setGatewayPort(port)                        
        try:                                                                            
            execute(lambda: _runGateway(commands, os.path.dirname(__file__)), "Cloning")                                                          
        except Py4JConnectionException:            
            startGateway()
            execute(lambda: _runGateway(commands, os.path.dirname(__file__)), "Cloning")  

_repos = {}

def createRepository(url, init = False):
    global _repos
    connector = PyQtConnectorDecorator()
    connector.checkIsAlive()    
    if url in _repos:
        if init:
            raise GeoGitException("There is already a tracked repository in that location")
        else:
            return _repos[url]
    else:
        if init and os.path.exists(os.path.join(url, ".geogit")):
            raise GeoGitException("The selected path already contains a GeoGit repository")            
        repo = Repository(url, connector, init)
        if not init:
            _repos[url] = repo
        return repo

def removeFromRepositoryPool(url):
    global _repos
    if url in _repos:
        del _repos[url]
            
_proc = None

def startGateway():
    global _proc
    _logger.debug("GeoGit gateway not started. Will try to start it")
    if not os.path.exists(geogitPath()):
        _logger.debug("GeoGit path (%s) does not exist. Cannot start gateway" % geogitPath())
        return                 
    try:         
        _logger.debug("Trying to start gateway at %s" % (geogitPath()))   
        if os.name == 'nt':
            _proc = subprocess.Popen([os.path.join(geogitPath() , "geogit-gateway.bat")], shell = True)
        else:
            _proc = subprocess.Popen(os.path.join(geogitPath(), "geogit-gateway"), stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        time.sleep(3) #improve this and wait until the "server started" string is printed out                            
        port = config.getConfigValue(config.GENERAL, config.GATEWAY_PORT) 
        gateway = JavaGateway(GatewayClient(port = port))
        gateway.entry_point.isGeoGitServer()   
        _logger.error("Gateway correctly started")                 
    except Exception, e:
        _logger.error("Could not start gateway (%s)" % (str(e)))
        _proc = None
        
def killGateway():
    global _proc            
    if _proc is not None:
        _logger.debug("Killing gateway process")
        if os.name == 'nt':            
            subprocess.Popen("TASKKILL /F /PID " + str(_proc.pid) + " /T", shell = True)
        else:
            os.kill(_proc.pid, signal.SIGKILL)        
        _proc = None
        
     
