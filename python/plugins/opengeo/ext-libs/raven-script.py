#!c:\python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'raven==3.5.1','console_scripts','raven'
__requires__ = 'raven==3.5.1'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('raven==3.5.1', 'console_scripts', 'raven')()
)
