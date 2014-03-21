FILE(GLOB INSTALLER_FILES *.asc *.shp *.geojson *.qgs *.dbf *.prj *.qpj *.shx *.xml)

PLUGIN_INSTALL(opengeo test/data ${INSTALLER_FILES})
