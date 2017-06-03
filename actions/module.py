from __future__ import absolute_import,division,print_function,unicode_literals

from functools import partial

from lib.action import Action

from app import app


toolbar_visible = True

actions = [['file', 'Load File Actions'],
           ['edit', 'Load Edit Actions'],
           ['view', 'Load View Actions'],
           ['option', 'Load Option Actions'],
           ['help', 'Load Help Actions'],
           ['test', 'Load Test Actions'],
           ['unit_test', 'Load Unit Test Actions'],
           ['my_actions', 'Load My Actions']
          ]

tools = [['select', 'Load Select Tool'],
         ['delete', 'Load Delete Tool'],
         ['primitives', 'Load Primitives Tools'],
         ['transform', 'Load Transfrom Tools'],
         ['expand', 'Load Expand Tools'],
         ['boolean', 'Load Boolean Tools'],
         ['test', 'Load Test Tools']
        ]

list = []

for action, menu in actions:
    ac = Action(partial(app.load_actions, 'actions.'+action),
                ['&Modules', menu])
    list.append(ac)

for tool, menu in tools:
    ac = Action(partial(app.load_tools, 'tools.'+tool), ['&Modules', menu])
    list.append(ac)
