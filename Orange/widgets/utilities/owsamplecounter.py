# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import SampleCounter


class OWSampleCounter(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Count Samples"
    description = "Add a sample counter channels."
    author = "Christian Kothe"
    icon = "icons/SampleCounter.svg"
    priority = 14
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
    enabled = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SampleCounter())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('enabled', self.node.enabled)
        else:
            self.node.enabled = self.enabled

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.enabled_control = gui.checkBox(box, self, 'enabled', label='Enabled', callback=lambda: self.property_changed('enabled'), tooltip="Whether this stage is enabled.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
