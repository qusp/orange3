# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import OverrideTimestamps


class OWOverrideTimestamps(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Override Timestamps"
    description = "Override time stamps based on the system clock and the sampling rate."
    author = "Christian Kothe (ckothe@ucsd.edu)"
    icon = "icons/OverrideTimestamps.svg"
    priority = 12
    category = "Utilities"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': builtins.object, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': builtins.object, 'flags': 0},
    ]

    # Configuration properties.

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(OverrideTimestamps())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            pass
        else:
            pass

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
