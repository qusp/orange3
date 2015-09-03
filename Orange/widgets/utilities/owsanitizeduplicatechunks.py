# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import SanitizeDuplicateChunks


class OWSanitizeDuplicateChunks(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Sanitize Duplicate Chunks"
    description = "Remove successive duplicate chunks from the data.."
    author = "Christian Kothe"
    icon = "icons/SanitizeDuplicateChunks.svg"
    priority = 15
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
    show_warnings = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SanitizeDuplicateChunks())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('show_warnings', self.node.show_warnings)
        else:
            self.node.show_warnings = self.show_warnings

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.show_warnings_control = gui.checkBox(box, self, 'show_warnings', 'Show warnings', callback=lambda: self.property_changed('show_warnings'), tooltip="Show warnings when dropping chunks.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
