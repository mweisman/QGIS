import os
import sys
import inspect
from geogit import config
import traceback
import shutil
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from geogit.tools.utils import userFolder
from gui.dialogs.configdialog import ConfigDialog
from geogit.gui.dialogs.geogiterrordialog import GeoGitErrorDialog
from geogitpy.py4jconnector import Py4JConnectionException
from geogit.gui.viewer import GeoGitViewer
from geogitpy.geogitexception import GeoGitException, InterruptedOperationException 
from geogit.tools.utils import tempFolder
from geogit.tools.infotool import MapToolGeoGitInfo
from geogit.tools.layertracking import readTrackedLayers
from geogit.tools.layertracker import LayerTracker
from geogit.gui.dialogs import reposelector
from py4j.protocol import Py4JNetworkError
from geogit.gui.dialogs.addlayerdialog import AddGeoGitLayerDialog
from geogit.gui.dialogs.gatewaynotavailabledialog import GatewayNotAvailableDialog
import subprocess
from geogit.gui.pyqtconnectordecorator import killGateway

cmd_folder = os.path.split(inspect.getfile( inspect.currentframe()))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

logger = logging.getLogger("geogitpy")

class GeoGitPlugin:
    
    geogitPath = os.path.join(os.path.dirname(QgsApplication.qgisUserDbFilePath()), 
                                "python", "plugins", "geogit", "apps" ,"geogit", "bin")

    def __init__(self, iface):
        self.iface = iface
        config.iface = iface
                                    
        self.explorer = None
                        
        logFile = os.path.join(userFolder(), "geogitpy.log")
        handler = logging.FileHandler(logFile)                
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler) 
        
        QgsMapLayerRegistry.instance().layersAdded.connect(self.layersAdded)
        self.tracker = LayerTracker()  
                
    def unload(self):
        self.menu.deleteLater()          
        sys.excepthook = self.qgisHook
        
        killGateway()
        
        #delete temporary output files
        folder = tempFolder()
        if QDir(folder).exists():
            shutil.rmtree(folder, True)

    def initGui(self):      
        
        icon = QIcon(os.path.dirname(__file__) + "/ui/resources/geogit.png")
        self.addLayerAction = QAction(icon, "Add GeoGit layer...", self.iface.mainWindow())
        self.addLayerAction.triggered.connect(self.addLayer)
        menu = self.iface.layerMenu()
        actions = menu.actions()
        menu.insertAction(actions[6], self.addLayerAction)
        for subaction in actions:            
            if subaction.isSeparator():               
                menu.insertAction(subaction, self.addLayerAction)       
                break

        self.menu = QMenu(self.iface.mainWindow())
        self.menu.setTitle("GeoGit")       
        icon = QIcon(os.path.dirname(__file__) + "/ui/resources/geogit.png")
        self.explorerAction = QAction(icon, "GeoGit client", self.iface.mainWindow())
        self.explorerAction.triggered.connect(self.openExplorer)
        self.menu.addAction(self.explorerAction)
        icon = QIcon(os.path.dirname(__file__) + "/ui/resources/config.png")
        self.configAction = QAction(icon, "GeoGit client settings", self.iface.mainWindow())
        self.configAction.triggered.connect(self.openSettings)
        self.menu.addAction(self.configAction)
        icon = QIcon(os.path.dirname(__file__) + "/ui/resources/identify.png")
        self.toolAction = QAction(icon, "GeoGit feature info tool", self.iface.mainWindow())
        self.toolAction.setCheckable(True)
        self.toolAction.triggered.connect(self.setTool)
        self.menu.addAction(self.toolAction)
        
        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)
                                        
        self.qgisHook = sys.excepthook;    

        def pluginHook(t, value, tb):            
            if isinstance(value, GeoGitException):                
                logger.error(unicode(tb))
                self.setWarning(unicode(value))
            elif isinstance(value, (Py4JConnectionException, Py4JNetworkError)):                             
                dlg = GatewayNotAvailableDialog(self.iface.mainWindow())
                dlg.exec_()
            else:
                trace = "".join(traceback.format_exception(t, value, tb))
                if "geogit" in trace.lower():
                    dlg = GeoGitErrorDialog(trace, self.iface.mainWindow())
                    dlg.exec_()
                else:
                    self.qgisHook(t, value, tb)                                       
        sys.excepthook = pluginHook      
        
        self.mapTool = MapToolGeoGitInfo(self.iface.mapCanvas())                  
        #This crashes QGIS, so we comment it out until finding a solution
        #self.mapTool.setAction(self.toolAction)
        
        readTrackedLayers()                     


            
    
    def setWarning(self, msg):
        QMessageBox.warning(None, 'Could not complete GeoGit command',
                msg, 
                QMessageBox.Ok)        
        

    def setTool(self):
        self.toolAction.setChecked(True)
        self.iface.mapCanvas().setMapTool(self.mapTool)
        
    def addLayer(self):
        dlg = AddGeoGitLayerDialog(self.iface.mainWindow())
        dlg.exec_()
    
    def openExplorer(self): 
        config.iface = self.iface                      
        repo = reposelector.getRepo()
        if repo is not None:
            repo.repo.connector.checkIsAlive()
            if self.explorer is None:   
                self.explorer = GeoGitViewer(repo) 
                config.explorer = self.explorer                               
                self.iface.addDockWidget(Qt.RightDockWidgetArea, self.explorer)           
                self.explorer.show()
            else:
                self.explorer.setRepo(repo)
                self.explorer.show()

        
    def openSettings(self):
        dlg = ConfigDialog()
        dlg.exec_()
        
    def layersAdded(self, layers):
        for layer in layers:  
            if layer.type() == layer.VectorLayer:                                                      
                self.tracker.trackLayer(layer)          
        

                