INCLUDE ("@CMAKE_BINARY_DIR@/mac/0vars.cmake")
INCLUDE ("@CMAKE_SOURCE_DIR@/cmake/MacBundleMacros.cmake")

# Global lib paths
SET (BUILD_LIB_PATH "/opt/qgis_deps/lib")
SET (BUNDLE_LIB_PATH "@executable_path/lib")
SET (GRASS_BUILD_PATH "/opt/qgis_deps/grass-6.4.3")
SET (GRASS_BUNDLE_PATH "@executable_path/grass")

# Same as global INSTALLNAMETOOL_CHANGE but errors are silenced so we don't get bombarded with errors on directories
FUNCTION (INSTALLNAMETOOL_CHANGE_NO_ERR CHANGE CHANGETO CHANGEBIN)
    IF (EXISTS "${CHANGEBIN}" AND CHANGE AND CHANGETO)
        # ensure CHANGEBIN is writable by user, e.g. Homebrew binaries are installed non-writable
        EXECUTE_PROCESS (COMMAND chmod u+w "${CHANGEBIN}")
        EXECUTE_PROCESS (COMMAND install_name_tool -change ${CHANGE} ${CHANGETO} "${CHANGEBIN}" ERROR_QUIET)
    ENDIF ()
ENDFUNCTION (INSTALLNAMETOOL_CHANGE_NO_ERR)


# Modified version of global GET_INSTALL_NAME
FUNCTION (INSTALL_NAME LIBFILE OUTVAR)
    IF (EXISTS "${LIBFILE}")
        EXECUTE_PROCESS (COMMAND otool -D "${LIBFILE}" OUTPUT_VARIABLE iname_out)
        # Extract second line of output which contains the lib id
        STRING (REGEX REPLACE ".*:\n" "" iname "${iname_out}")
        # Make sure there is an actual install name
        STRING (COMPARE EQUAL "${iname}" "" result)
        IF (result)
            SET ("" out)
        ELSE()
            STRING (STRIP ${iname} out)
        ENDIF()
        SET (${OUTVAR} ${out} PARENT_SCOPE)
    ELSE ()
        SET (${OUTVAR} "" PARENT_SCOPE)
    ENDIF ()
ENDFUNCTION (INSTALL_NAME)

# Ensure IDs are correct
FUNCTION (INSTALLNAMETOOL_SET_ID ID LIBRARY)
    IF (EXISTS "${LIBRARY}" AND ID)
        EXECUTE_PROCESS (COMMAND chmod u+w "${LIBRARY}")
        EXECUTE_PROCESS (COMMAND install_name_tool -id ${ID} "${LIBRARY}")
    ENDIF ()
ENDFUNCTION (INSTALLNAMETOOL_SET_ID)

# Ensure bundled dylibs all point to the right place. Based on global UPDATEQGISPATHS fn.
FUNCTION (UPDATELOCALPATHS LIBFROM LIBTO)
        # Update the lib path for dylibs in /lib
        FILE (GLOB files "${QLIBDIR}/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        
        # Update the lib path for bins in /bin
        FILE (GLOB files "${QLIBDIR}/../bin/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        
        # Update the lib path for dylibs in framework root
        FILE (GLOB files "${QFWDIR}/*.framework/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        
        # Update the lib path for dylibs in framework internals
        FILE (GLOB files "${QFWDIR}/*.framework/Versions/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        
        # Update lib paths for grass
        FILE (GLOB files "${QLIBDIR}/../grass/bin/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        FILE (GLOB files "${QLIBDIR}/../grass/driver/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        FILE (GLOB files "${QLIBDIR}/../grass/driver/db/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        FILE (GLOB files "${QLIBDIR}/../grass/etc/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        FILE (GLOB files "${QLIBDIR}/../grass/lib/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
        FILE (GLOB files "${QLIBDIR}/../grass/tools/*")
        FOREACH (file ${files})
            INSTALLNAMETOOL_CHANGE_NO_ERR(${LIBFROM} ${LIBTO} ${file})
        ENDFOREACH()
ENDFUNCTION (UPDATELOCALPATHS)

# re-link libs
# TODO: figure out why wildcards don't work in COMMAND so we can get rid of this loop.
MESSAGE (STATUS "Copying dylibs to ${QLIBDIR}...")
FILE (GLOB files "${BUILD_LIB_PATH}/*.dylib")
FOREACH (build_file ${files})
  EXECUTE_PROCESS (COMMAND ditto "${build_file}" "${QLIBDIR}")
ENDFOREACH ()

# Unclear why this dylib does not get copied in above loop
EXECUTE_PROCESS (COMMAND cp "${BUILD_LIB_PATH}/libgeos_c.1.dylib" "${QLIBDIR}")

# Copy GDAL binaries for processing
MESSAGE (STATUS "Copying gdal...")
FILE (GLOB gdal_binaries "${BUILD_LIB_PATH}/../bin/gdal*")
FOREACH (bin ${gdal_binaries})
  EXECUTE_PROCESS (COMMAND ditto ${bin} "${QLIBDIR}/../bin")
ENDFOREACH ()
FILE (GLOB ogr_binaries "${BUILD_LIB_PATH}/../bin/ogr*")
FOREACH (bin ${ogr_binaries})
  EXECUTE_PROCESS (COMMAND ditto ${bin} "${QLIBDIR}/../bin")
ENDFOREACH ()

MESSAGE (STATUS "Copying grass...")
EXECUTE_PROCESS (COMMAND cp -r "${GRASS_BUILD_PATH}" "${QLIBDIR}/../grass")
EXECUTE_PROCESS (COMMAND mkdir "${QLIBDIR}/../share")
EXECUTE_PROCESS (COMMAND cp -r "${BUILD_LIB_PATH}/../share/gdal" "${QLIBDIR}/../share/gdal")

# re-link grass
MESSAGE (STATUS "Re-linking grass libs...")
FILE (GLOB grass_dirs "${QLIBDIR}/../grass/*")
FOREACH (dir ${grass_dirs})
  EXECUTE_PROCESS (COMMAND basename "${dir}" OUTPUT_VARIABLE dir_basename_newline)
  # Strip newline from end of dirname
  STRING (STRIP ${dir_basename_newline} dir_basename)
  # grab files in dir
  FILE (GLOB files "${dir}/*")
  FOREACH (file ${files})
    EXECUTE_PROCESS (COMMAND basename "${file}" OUTPUT_VARIABLE file_basename_newline)
    STRING (STRIP ${file_basename_newline} file_basename)
    MESSAGE (STATUS "Re-linking ${file_basename}")
    get_filename_component(bundle_file "${QLIBDIR}/../grass/${dir_basename}/${file_basename}" REALPATH)
    SET(BUNDLE_ID "${GRASS_BUNDLE_PATH}/${dir_basename}/${file_basename}")
    INSTALL_NAME ("${bundle_file}" OLD_LIB_INSTALL_NAME)
    # No install name means nothing can link to it. Don't try to re-link.
    STRING (COMPARE NOTEQUAL "${OLD_LIB_INSTALL_NAME}" "" result)
    IF (result)
        INSTALLNAMETOOL_SET_ID (${BUNDLE_ID} "${bundle_file}")
        UPDATELOCALPATHS ("${OLD_LIB_INSTALL_NAME}" "${BUNDLE_ID}")
        UPDATEQGISPATHS ("${OLD_LIB_INSTALL_NAME}" "../grass/lib/${file_basename}")
    ENDIF()
  ENDFOREACH()
ENDFOREACH()

# For some reason geos isn't getting re-linked. Force it here
FILE (GLOB grass_libs "${QLIBDIR}/../grass/lib/*.dylib")
FOREACH (lib ${grass_libs})
  INSTALLNAMETOOL_CHANGE("/opt/qgis_deps/lib/libgeos.3.4.2.dylib" "@executable_path/lib/libgeos.3.4.2.dylib" "${lib}")
  INSTALLNAMETOOL_CHANGE("/opt/qgis_deps/lib/libgeos_c.1.dylib" "@executable_path/lib/libgeos_c.1.dylib" "${lib}")
ENDFOREACH ()

FILE (GLOB_RECURSE files FOLLOW_SYMLINKS "${QLIBDIR}/*.dylib")
FOREACH (file ${files})
  EXECUTE_PROCESS (COMMAND basename "${file}" OUTPUT_VARIABLE file_basename_newline)
  # Strip newline from end of filename
  STRING (STRIP ${file_basename_newline} file_basename)
  MESSAGE (STATUS "Re-linking ${file_basename}...")
  SET(bundle_file "${QLIBDIR}/${file_basename}")
  SET(BUNDLE_ID "${BUNDLE_LIB_PATH}/${file_basename}")
  INSTALL_NAME ("${bundle_file}" LIB_INSTALL_NAME)
  INSTALLNAMETOOL_SET_ID (${BUNDLE_ID} "${bundle_file}")
  UPDATEQGISPATHS (${LIB_INSTALL_NAME} ${file_basename})
  UPDATELOCALPATHS (${LIB_INSTALL_NAME} ${BUNDLE_ID})
  # Some things get linked without a dir. Add the loader_path to those.
  UPDATEQGISPATHS (${file_basename} ${file_basename})
  UPDATELOCALPATHS (${file_basename} ${BUNDLE_ID})
ENDFOREACH ()

# libqscintilla has some links to the QT build location. Change those to internal frameworks
FILE (GLOB files "${QLIBDIR}/libqscintilla*.dylib")
FOREACH (qscilib ${libs})
  INSTALLNAMETOOL_CHANGE("/usr/local/Trolltech/Qt-4.8.5/lib/QtGui.framework/Versions/4/QtGui" "@executable_path/../Frameworks/QtGui.framework/QtGui" "${qscilib}")
  INSTALLNAMETOOL_CHANGE("@loader_path/../../Frameworks/QtGui.framework/QtGui" "@executable_path/../Frameworks/QtGui.framework/QtGui" "${qscilib}")
  INSTALLNAMETOOL_CHANGE("@loader_path/../../Frameworks/QtCore.framework/QtCore" "@executable_path/../Frameworks/QtCore.framework/QtCore" "${qscilib}")
  INSTALLNAMETOOL_CHANGE("/usr/local/Trolltech/Qt-4.8.5/lib/QtCore.framework/Versions/4/QtCore" "@executable_path/../Frameworks/QtCore.framework/QtCore" "${qscilib}")
ENDFOREACH ()

# Setup python utils
MESSAGE (STATUS "Setting up psycopg2...")
EXECUTE_PROCESS (COMMAND cp -r "${BUILD_LIB_PATH}/../python/site-packages/psycopg2" "${QLIBDIR}/../../Resources/python/.")
MESSAGE (STATUS "Setting up osgeo...")
EXECUTE_PROCESS (COMMAND cp -r "${BUILD_LIB_PATH}/../python/site-packages/osgeo" "${QLIBDIR}/../../Resources/python/.")
# Need to relink the osgeo libs to point to the internal gdal.dylib
FILE (GLOB osgeo_libs "${QLIBDIR}/../../Resources/python/osgeo/*.so")
FOREACH (lib ${osgeo_libs})
  INSTALLNAMETOOL_CHANGE("${BUILD_LIB_PATH}/libgdal.1.dylib" "${BUNDLE_LIB_PATH}/libgdal.1.dylib" "${lib}")
ENDFOREACH ()
