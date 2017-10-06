import sys
from os import path

# add the package directory to sys.path
# this ensures that the application will work if it is intalled through
#    "python setup.py develop --user"
sys.path.append(path.dirname(__file__))

from os import path as _path
from appclass import KubosApp as _KubosApp

"""This module holds the application object, which is an instance of
KubosApp.
Importing this module will create an application and start the event loop.
"""

_file = _path.dirname(_path.abspath(__file__))
app = _KubosApp(appdir=_file)

app.run()
