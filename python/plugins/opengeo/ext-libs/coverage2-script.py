#!c:\python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'coverage==3.7','console_scripts','coverage2'
__requires__ = 'coverage==3.7'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('coverage==3.7', 'console_scripts', 'coverage2')()
)
