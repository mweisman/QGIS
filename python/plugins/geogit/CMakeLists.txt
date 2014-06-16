FILE(GLOB INSTALLER_FILES *.py)

PLUGIN_INSTALL(geogit . ${INSTALLER_FILES} __init__.py metadata.txt)

# We don't need to properly install the ext-libs or geogit itself as plugins, just need to drop them in place.
INSTALL (DIRECTORY ext-libs DESTINATION ${QGIS_DATA_DIR}/python/plugins/geogit/.)
INSTALL (DIRECTORY apps DESTINATION ${QGIS_DATA_DIR}/python/plugins/geogit/.)

ADD_SUBDIRECTORY(gui)
ADD_SUBDIRECTORY(resources)
ADD_SUBDIRECTORY(tools)
ADD_SUBDIRECTORY(ui)
