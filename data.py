# -*- coding: UTF-8 -*-
from OCC import TopoDS
from lib import gp_
from lib.appdata import Appdata
import std_events

appdata = Appdata()

def on_doc_modified():
    appdata.set('dirty', True)

std_events.document_modified.connect(on_doc_modified)


def on_dirty_set(value):
    if appdata.get('dirty') != value:
        appdata.sset('dirty', value)
        std_events.dirty_changed.emit()

def on_filename_set(value):
    if appdata.get('filename') != value:
        appdata.sset('filename', value)
        std_events.filename_changed.emit()

def on_input_set(new_input):
    # Emit a signal if the new input is different from the previous one
    input_changed = False
    if isinstance(new_input, gp_.gp_Pnt_):
        if appdata.get('input') != new_input:
            input_changed = True
    elif isinstance(new_input, TopoDS.TopoDS_Shape):
        if appdata.get('input') is None:
            input_changed = True
        elif not new_input.IsSame(appdata.get('input')):
            input_changed = True
        # TODO: Currently the preview is always removed and redisplayed
        # on every input change in order to avoid it being selected.
        # Make it unselectable.
        else:
            input_changed = True
    elif new_input is None:
        if appdata.get('input') is not None:
            input_changed = True
    else:
        raise TypeError('unsupported type for "input". Only None, gp_Pnt_ '
                        'and TopoDS_Shape are supported')
    if input_changed:
        appdata.sset('input', new_input)
        std_events.input_changed.emit()


appdata.add('APPLICATION_NAME')
appdata.set('APPLICATION_NAME', 'CAD application')
appdata.add('AUTHORS')
appdata.add('QUALITY')
appdata.add('VERSION')

appdata.add('APPDIR')
appdata.add('dirty', on_set=on_dirty_set)
appdata.add('filename', on_set=on_filename_set)
appdata.set('filename', '')
appdata.add('input', on_set=on_input_set)
appdata.add('input_valid')
appdata.set('input_valid', False)
appdata.add('mode')
appdata.add('active_plane')
appdata.set('active_plane', 2)
appdata.add('icon')
