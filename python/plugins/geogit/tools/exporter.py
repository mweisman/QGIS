'''
This module provides methods to export layers so they can be used as valid data 
for importing to GeoGit.

It also includes method to export from GeoGit to QGIS
'''

import os
import utils
import logging
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from geogitpy.geogitexception import GeoGitException
from geogit.tools.utils import tempFilenameInTempFolder
from geogit.tools.layertracking import addTrackedLayer

_logger = logging.getLogger("geogitpy")
    
def exportVectorLayer(layer, addId):
    '''accepts a QgsVectorLayer'''
    settings = QSettings()
    systemEncoding = settings.value( "/UI/encoding", "System" )    
    filename = unicode(layer.source())  
    destFilename = unicode(layer.name())                        
    if not filename.lower().endswith("shp") or addId: 
        output = utils.tempFilenameInTempFolder(destFilename + ".shp")
        provider = layer.dataProvider()
        fields = layer.pendingFields()  
        if addId:
            fields.append(QgsField("id", QVariant.String))        
        writer = QgsVectorFileWriter(output, systemEncoding, fields, provider.geometryType(), layer.crs())
        for i, feat in enumerate(layer.getFeatures()):
            if addId:
                attribs = feat.attributes()
                attribs.append(str(i+1))
                feat.setAttributes(attribs)
            writer.addFeature(feat)
        del writer
        return output
    else:
        return filename


def exportFromGeoGitToTempFile(repo, ref, path):
    #try to import as spatialite (might not work in if sl drivers are not available)        
    failed = False
    try:
        filepath = tempFilenameInTempFolder("export.sqlite")
        repo.exportsl(ref, path, filepath, table = path)
        uri = QgsDataSourceURI()
        uri.setDatabase(filepath)                                    
        uri.setDataSource('', path, 'the_geom')
        layer = QgsVectorLayer(uri.uri(), path, 'spatialite')
        failed = not layer.isValid()
        _logger.debug("Layer %s exported to spatialite database %s, but could not be opened" % (path, filepath))
    except GeoGitException:
        _logger.debug("Could not export layer %s to spatialite database %s" % (path, filepath))
        failed = True;
    
    if failed:
        filepath = tempFilenameInTempFolder("export.shp")
        repo.exportshp(ref, path, filepath)                   
        layer = QgsVectorLayer(filepath, path, "ogr")                            
    
    hasField = False
    fields = layer.pendingFields().toList()        
    for field in fields:
        if field.name().lower() == "id":
            hasField = True
            break    
    
    QgsMapLayerRegistry.instance().addMapLayers([layer])                                
    addTrackedLayer(repo.url, layer.source(), path)
    return hasField



