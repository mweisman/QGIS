from PyQt4.QtCore import *

iface = None
explorer = None

GENERAL = "General"

ADVANCED_UI = "AvancedUI"                         
CLONE_PARENT_PATH = "CloneParentPath"
CLONE_DIRECTLY = "CloneDirectly"
USE_THREADS = "UseThreads"
AUTO_UPDATE = "AutoUpdate"
GATEWAY_PORT = "GatewayPort"
SHOW_MESSAGE_ON_SMART_UPDATE_FAIL = "ShowUpdateFaiMessage"

generalParams = [(ADVANCED_UI, "Show advanced interface (requires restart)", False),                         
                 (CLONE_PARENT_PATH, "Preferred parent path for Ujo cloned repositories", ""),
                 (CLONE_DIRECTLY, "Clone directly into preferred path without asking", False),
                 (AUTO_UPDATE, "Automatically import tracked layers after they are edited", True),
                 (GATEWAY_PORT, "Port for GeoGit gateway", 25333),
                 (SHOW_MESSAGE_ON_SMART_UPDATE_FAIL, "Show warning message on smart update failure", True)]
                          
def getConfigValue(group, name):
    default = None
    for param in generalParams:
        if param[0] == name:
            default = param[2]
    
    if isinstance(default, bool):
        return QSettings().value("/GeoGit/Settings/%s/%s" % (group, name), default, bool)
    else:
        return QSettings().value("/GeoGit/Settings/%s/%s" % (group, name), default, str) 
