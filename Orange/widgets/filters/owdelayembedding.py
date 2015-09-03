# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import DelayEmbedding


class OWDelayEmbedding(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Delay Embedding"
    description = "Perform delay embedding of the given signal; this will create a new axis of type LagAxis (which can be folded into other axes using a separate node."
    author = "Christian Kothe"
    icon = "icons/DelayEmbedding.svg"
    priority = 3
    category = "Filters"

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
    lags = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(DelayEmbedding())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('lags', self.node.lags)
        else:
            self.node.lags = self.lags

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.lags_control = gui.lineEdit(box, self, 'lags', label='Lags:', orientation='horizontal', callback=lambda: self.property_changed('lags'), tooltip="Lags to use. This is a sequence of positive offsets in samples, referring to past samples. Default: (0, 1, 2, 3).")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
