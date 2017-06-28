# -*- coding: UTF-8 -*-
#convert to Python 3
# TODO: check occurences of document_modified.emit(), reduce them
from data import appdata
from app import app
from lib import argparse

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
    appdata.set('APPLICATION_NAME', 'Kubos '+appdata.get('mode').title())


app.exec_()
