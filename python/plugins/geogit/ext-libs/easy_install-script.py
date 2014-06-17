#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'setuptools==5.1','console_scripts','easy_install'
__requires__ = 'setuptools==5.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('setuptools==5.1', 'console_scripts', 'easy_install')()
    )
