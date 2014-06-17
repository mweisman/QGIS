# -*- coding: utf-8 -*-

import sys
import os
import site

site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

def classFactory(iface):
    from geogit.plugin import GeoGitPlugin
    return GeoGitPlugin(iface)
