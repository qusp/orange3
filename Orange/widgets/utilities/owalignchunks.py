# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import AlignChunks


class OWAlignChunks(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Align Chunks"
    description = "Turn interleaved multi-modal chunks into chunks with time-aligned data."
    author = "Christian Kothe"
    icon = "icons/AlignChunks.svg"
    priority = 2
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
    max_marker_lag = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(AlignChunks())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('max_marker_lag', self.node.max_marker_lag)
        else:
            self.node.max_marker_lag = self.max_marker_lag

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.max_marker_lag_control = gui.lineEdit(box, self, 'max_marker_lag', label='Max marker lag:', orientation='horizontal', callback=lambda: self.property_changed('max_marker_lag'), tooltip="Maximum marker delivery lag. This is the maximum delay (in seconds) with which markers may show up in the input packet. If marker streams are present, this will be the minimum wall-clock delay of the output stream.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
