from __future__ import absolute_import,division,print_function,unicode_literals

from os import path

from data import appdata

# application directory
appdata.set('APPDIR', path.dirname(__file__))

appdata.set('mode', 'standard')
appdata.set('APPLICATION_NAME', 'Kubos')

from app import app

app.load_actions('actions.view')

app.exec_()
