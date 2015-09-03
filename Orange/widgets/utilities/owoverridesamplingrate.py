# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import OverrideSamplingRate


class OWOverrideSamplingRate(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Override Sampling Rate"
    description = "Override the sampling rate in the given data's time axis."
    author = "Christian Kothe"
    icon = "icons/OverrideSamplingRate.svg"
    priority = 11
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
    sampling_rate = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(OverrideSamplingRate())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('sampling_rate', self.node.sampling_rate)
        else:
            self.node.sampling_rate = self.sampling_rate

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.sampling_rate_control = gui.lineEdit(box, self, 'sampling_rate', label='Sampling rate:', orientation='horizontal', callback=lambda: self.property_changed('sampling_rate'), tooltip="Sampling rate override. Sets the assumed sampling rate of the axis to filter (particularly useful when filtering non-time axes). Default: None.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
