# -*- coding: UTF-8 -*-

#convert to Python 3

# TODO: check occurences of document_modified.emit(), reduce them

import data
from data import *
from app import *


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
if data.appdata.get('mode') == 'standard':
    appdata.set('APPLICATION_NAME', 'Kubos')
else:
    appdata.set('APPLICATION_NAME', 'Kubos '+data.appdata.get('mode').title())


app.exec_()
