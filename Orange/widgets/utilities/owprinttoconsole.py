# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import PrintToConsole


class OWPrintToConsole(cpewidget.CPEWidget):

    # Node meta-data.
    name = "PrintToConsole"
    description = "Print input data to the Python console."
    author = "Christian Kothe"
    icon = "icons/PrintToConsole.svg"
    priority = 13
    category = "Utilities"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    only_nonempty = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(PrintToConsole())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('only_nonempty', self.node.only_nonempty)
        else:
            self.node.only_nonempty = self.only_nonempty

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.only_nonempty_control = gui.checkBox(box, self, 'only_nonempty', label='Only nonempty', callback=lambda: self.property_changed('only_nonempty'), tooltip="Only print non-empty packets.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
