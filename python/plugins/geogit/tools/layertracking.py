import os
from qgis.core import *
from geogit.tools.utils import userFolder
import json
from json.decoder import JSONDecoder
from json.encoder import JSONEncoder
tracked = []

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def decoder(jsonobj):
    if 'host' in jsonobj:
        return TrackedDatabase(jsonobj['host'], jsonobj['database'], jsonobj['port'], 
                            jsonobj['schema'], jsonobj['url'], jsonobj['dest'])
    elif 'source' in jsonobj:
        return TrackedLayer(jsonobj['source'], jsonobj['url'], jsonobj['dest']) 
    else:
        return jsonobj 
           
class TrackedObject(object):             
    pass
    
class TrackedLayer(TrackedObject):        
    def __init__(self, source, url, dest):
        self.url = url
        self.dest = dest
        self.source = source        

class TrackedDatabase(TrackedObject):        
    def __init__(self, host, database, port, schema, url, dest):
        self.url = url
        self.dest = dest
        self.host = host
        self.database = database
        self.port = port
        self.schema = schema


def addTrackedLayer(url, source, dest = None):
    global tracked
    source = os.path.normcase(source)    
    layer = TrackedLayer(source, url, dest)  
    tracked.append(layer) 
    saveTracked()    

def addTrackedDatabase(url, host, database, port, schema, dest):
    global tracked
    layer = TrackedDatabase(host, database, port, schema, url, dest)  
    tracked.append(layer)
    saveTracked()
    
def saveTracked():
    filename = os.path.join(userFolder(), "layers")
    with open(filename, "w") as f:
        f.write(json.dumps(tracked, cls = Encoder))
    
def readTrackedLayers():      
    global tracked
    filename = os.path.join(userFolder(), "layers")    
    if os.path.exists(filename):
        with open(filename) as f:
            lines = f.readlines()
        jsonstring = "\n".join(lines)
        if jsonstring:
            tracked = JSONDecoder(object_hook = decoder).decode(jsonstring)
  
def isTracked(layer):    
    return getTrackingInfo(layer) is not None

def getTrackingInfo(layer):
    source = layer.source()
    isPostGis = layer.dataProvider().name() == "postgres"
    for obj in tracked:
        if isinstance(obj, TrackedLayer):
            if obj.source == os.path.normcase(source):
                return obj.url, obj.dest
        elif isPostGis and isinstance(obj, TrackedDatabase):            
            provider = layer.dataProvider()
            uri = QgsDataSourceURI(provider.dataSourceUri())                                                                                                         
            if (obj.host == uri.host() and obj.database == uri.database() 
                    and obj.port == uri.port() and obj.schema == uri.schema()):
                dest = obj.dest or uri.table()
                return obj.url, dest
    return None
        
