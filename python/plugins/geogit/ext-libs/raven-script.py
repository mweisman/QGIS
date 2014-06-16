#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'raven==3.5.1','console_scripts','raven'
__requires__ = 'raven==3.5.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('raven==3.5.1', 'console_scripts', 'raven')()
    )
