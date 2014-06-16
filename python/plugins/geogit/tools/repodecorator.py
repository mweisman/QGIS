import os
from PyQt4 import QtGui
from geogit.gui.pyqtconnectordecorator import createRepository
from geogit.tools.utils import mkdir
import requests
from geogitpy.utils import prettydate
from geogit.gui import executor

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
        self.title = self.name    
        self.description = ""
        self.ujoUrl = None
        filename = os.path.join(self.url, "geogitpy", "ujo")
        if os.path.exists(filename):            
            with open(filename) as f:
                self.ujoUrl = f.next().strip()
                self.name = f.next().strip()
                self.title = f.next().strip()
                lines = []
                for line in f:
                    lines.append(line)
                self.description = "".join(lines)                      
        
    def setUjoData(self, ujoUrl, ujoName, ujoTitle, ujoDescription):
        self.name = ujoName
        self.title = ujoTitle
        self.description = ujoDescription
        self.ujoUrl = ujoUrl
        mkdir(os.path.join(self.url, "geogitpy"))
        filename = os.path.join(self.url, "geogitpy", "ujo")
        with open(filename, "w") as f:
            f.write(ujoUrl)
            f.write("\n")
            f.write(ujoName)
            f.write("\n")
            f.write(ujoTitle)
            f.write("\n")
            f.write(ujoDescription)
            f.write("\n")
        self._fullDescription = None
        
    def writeLayersFile(self):
        commands = ['ls-tree', "-v"]                    
        output = self.repo.connector.run(commands)
        mkdir(os.path.join(self.url, "geogitpy"))
        filename = os.path.join(self.url, "geogitpy", "layers")
        with open(filename, "w") as f:
            f.write(self.repo.head.id)
            for o in output:                    
                tokens = o.split(" ")
                f.write("\n")
                f.write(tokens[3] + " " + tokens[4])                
    
    def layers(self): 
        layers = {}                          
        filename = os.path.join(self.url, "geogitpy", "layers")
        if not os.path.exists(filename):
            try:
                self.writeLayersFile()
            except Exception, e:                
                return {}                                              
        else:
            with open(filename) as f:
                try:
                    headid = f.readline().strip()
                except:
                    headid = None
            if str(self.repo.head.id) != str(headid):
                try:
                    self.writeLayersFile()
                except Exception, e:                    
                    return {}
            with open(filename) as f:
                lines = f.readlines()[1:]                
                for line in lines:
                    tokens = line.split(" ")
                    layers[tokens[0]] = tokens[1]
        return layers      
                
            
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
            if self.title:
                s += "<p><b>TITLE: </b>%s</p>" % (self.title)
            if self.description:
                s += "<p><b>DESCRIPTION: </b>%s</p>" % (self.description)                            
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
            s += "<p><b>LAYERS</b>"
            s += "<ul>" + "".join(["<li>%s</li>" % lay for lay in self.layers()]) + "<ul>"
            s += "</p>"  
            if self.ujoUrl is not None:
                s += "<p><b>UPSTREAM UJO REPOSITORY: </b>%s</p>" % (self.ujoUrl)
                       
            self._fullDescription = s                        
                         
        return self._fullDescription
    
    def invalidateDescriptionCache(self):
        self._fullDescription = None
    
    @property
    def repo(self):
        if self._repo is None:
            self._repo = createRepository(self.url, False);
        return self._repo
    

class UjoRepository(object):
    
        
    def __init__(self, url, username, password, repoDefinition):
        self.url = url
        self.username = username
        self.password = password        
        self.name = repoDefinition.get("name", os.path.basename(self.url))
        self.title = repoDefinition.get("title", self.name)
        self.description = repoDefinition.get("description")        
        self.localClone = None
        self.lastModified = repoDefinition.get("updated")
        self.created = repoDefinition.get("created")
        self._collaborators = None
    
    
    @property
    def collaborators(self):
        if self._collaborators is None:
            def _getCollaborators():
                try:
                    r = requests.get(self.url + "/collaborators", auth=(self.username, self.password))                                
                    r.raise_for_status()
                    json = r.json()                    
                    return ["%s (%s)" % (c["fullName"], c["username"]) for c in json]
                except Exception, e:                         
                    return []                         
            self._collaborators = executor.execute(_getCollaborators)
        print self._collaborators
        return self._collaborators
    
    @property
    def icon(self):      
        return repoIcon
            
    @property
    def fullDescription(self):        
        s = "<p><b>NAME: </b>%s</p>" % (self.name)            
        s += "<p><b>TITLE: </b>%s</p>" % (self.title)            
        s += "<p><b>DESCRIPTION: </b>%s</p>" % (self.description)
        #s += "<p><b>URL: </b>%s</p>" % (self.url)         
        s += "<p><b>CREATED: </b>%s</p>" % (self.created) 
        s += "<p><b>LAST MODIFIED: </b>%s</p>" % (self.lastModified)                         
        if self.localClone is not None:
            s += "<p><b>CLONED LOCALLY AT: </b>%s</p>" % (self.localClone)
        if self.collaborators:            
            s += "<p><b>COLLABORATORS:</b>"
            s += "<ul>" + "".join(["<li>%s</li>" % c for c in self.collaborators]) + "<ul>"
            s += "</p>"            
        return s        
    
class InvalidRepoException(Exception):
    pass