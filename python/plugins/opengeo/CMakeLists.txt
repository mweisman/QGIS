FILE(GLOB INSTALLER_FILES *.py)

PLUGIN_INSTALL(opengeo . ${INSTALLER_FILES} __init__.py metadata.txt)

# We don't need to properly install the ext-libs as plugins, just need to drop them in place.
INSTALL (DIRECTORY ext-libs DESTINATION ${QGIS_DATA_DIR}/python/plugins/opengeo/.)

ADD_SUBDIRECTORY(geoserver)
ADD_SUBDIRECTORY(gui)
ADD_SUBDIRECTORY(images)
ADD_SUBDIRECTORY(postgis)
ADD_SUBDIRECTORY(qgis)
ADD_SUBDIRECTORY(resources)
ADD_SUBDIRECTORY(test)
