import os
from PyQt4 import QtGui
from geogit.gui.pyqtconnectordecorator import createRepository
from geogit.tools.utils import mkdir
import requests
from geogit.gui.executor import execute
from geogitpy.utils import prettydate

repoIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, "ui", "resources", "geogit-logo-24.png"))
wrongRepoIcon = QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                            os.pardir, "ui", "resources", "error.png"))

class LocalRepository(object):
    
    _repo = None
    _fullDescription = None
    
    def __init__(self, path):
        self.url = path
        self.name = os.path.basename(self.url)
        self.description = "No description available"
        
        
    @property
    def icon(self):
        if os.path.exists(os.path.join(self.url, ".geogit")):
            return repoIcon
        else:
            return wrongRepoIcon
        

        
    @property
    def fullDescription(self):
        if not os.path.exists(os.path.join(self.url, ".geogit")):
            raise InvalidRepoException()
        if self._fullDescription is None:
            s = "<p><b>NAME: </b>%s</p>" % (self.name)
            #s += "<p><b>DESCRIPTION: </b>%s</p>" % (self.description)
            s += "<p><b>LOCATION: </b>%s</p>" % self.url       
            try:
                lastCommit = self.repo.log(n = 1)[0]               
                lastModified = lastCommit.committerprettydate()
                lastMessage = lastCommit.message
            except Exception, e:                
                lastModified = "Not available"
                lastMessage = "Not available"
            s += "<p><b>LAST MODIFIED: </b>%s</p>" % (lastModified)
            s += "<p><b>LAST COMMIT MESSAGE: </b>%s</p>" % (lastMessage)             
                      
            self._fullDescription = s                        
                         
        return self._fullDescription
    
    def invalidateDescriptionCache(self):
        self._fullDescription = None
    
    @property
    def repo(self):
        if self._repo is None:
            self._repo = createRepository(self.url, False);
        return self._repo
    
class InvalidRepoException(Exception):
    pass