#!/usr/bin/python2
# -*- coding: UTF-8 -*-

# should work with Python 2.6 and 2.7, pythonOCC >= 0.5
# tested with:
#   Ubuntu, Python 2.7, pythonOCC 0.6 alpha
#   Windows, Python 2.6, pythonOCC 0.5
#   Debian 6, Python 2.6
#   Debian 7, Python 2.7, pythonOCC 0.6 alpha

# TODO: check occurences of document_modified.emit(), reduce them

# TODO: rename '__main__.pyw' -> 'main.pyw'

import os, sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from .data import appdata
from . import app

try:
    import argparse
except ImportError:
    from .lib import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    '--mode', choices=['standard', 'minimal', 'viewer', 'test', 'script'],
    help='Determines the tools and modules available on startup.')
parser.add_argument('URL', nargs='?', default='', help='Document to open')
args = parser.parse_args()
appdata.set('mode', args.mode or 'standard')
appdata.set('filename', args.URL)
if appdata.get('mode') == 'standard':
    appdata.set('APPLICATION_NAME', 'Kubos')
else:
    appdata.set('APPLICATION_NAME', 'Kubos ' + appdata.get('mode').title())


app.exec_()
