from PyQt5.QtWidgets  import QAction
from PyQt5.QtGui import QIcon


class Action(QAction):
    """Provides the same functionality as 'QAction', but with a simplified
    constructor and a different way of adding icons

    >>>Action(delete, ['&Edit', '&Delete'], icon='edit-delete')
    """
    def __init__(self, action, menu, group=None, icon=None, shortcut='',
                 tooltip=None, whats_this=None, checkable=False, checked=False,
                 enabled=True, parent=None):

        category, name = menu
        QAction.__init__(self, name, parent)

        self.category = category
        self.group = group
        self.triggered.connect(action)
        self.menu_name = name
        # the first action in a group decides on the location
        if icon and QIcon.hasThemeIcon(icon):
            self.setIcon(QIcon.fromTheme(icon))
        if tooltip:
            self.setToolTip(tooltip)
        if whats_this:
            self.setWhatsThis(whats_this)
        self.setCheckable(checkable)
        self.setChecked(checked)
        self.setShortcut(shortcut)
        self.setEnabled(enabled)
