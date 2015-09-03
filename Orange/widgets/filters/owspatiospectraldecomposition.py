# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import SpatioSpectralDecomposition


class OWSpatioSpectralDecomposition(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Spatio-Spectral Decomposition"
    description = "Filter the data using the spatio-spectral decomposition method."
    author = "Christian Kothe"
    icon = "icons/SpatioSpectralDecomposition.svg"
    priority = 14
    category = "Filters"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Peak Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_peak_data', 'flags': 0},
        {'name': 'Noise Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_noise_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Out Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    nof = Setting(None)
    streaming_update = Setting(None)
    half_time = Setting(None)
    shrinkage = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SpatioSpectralDecomposition())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('nof', self.node.nof)
            super().__setattr__('streaming_update', self.node.streaming_update)
            super().__setattr__('half_time', self.node.half_time)
            super().__setattr__('shrinkage', self.node.shrinkage)
        else:
            self.node.nof = self.nof
            self.node.streaming_update = self.streaming_update
            self.node.half_time = self.half_time
            self.node.shrinkage = self.shrinkage

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.nof_control = gui.lineEdit(box, self, 'nof', label='Nof:', orientation='horizontal', callback=lambda: self.property_changed('nof'), tooltip="Number of filters to learn.")
        self.streaming_update_control = gui.checkBox(box, self, 'streaming_update', label='Streaming update', callback=lambda: self.property_changed('streaming_update'), tooltip="Perform streaming (online) updates.")
        self.half_time_control = gui.lineEdit(box, self, 'half_time', label='Half time:', orientation='horizontal', callback=lambda: self.property_changed('half_time'), tooltip="Half time of exponentially weighted moving average filter. In seconds.")
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', label='Shrinkage:', orientation='horizontal', callback=lambda: self.property_changed('shrinkage'), tooltip="Regularization strength. This is primarily to prevent degenerate solutions.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_peak_data(self, peak_data):
        self.node.peak_data = peak_data

    def set_noise_data(self, noise_data):
        self.node.noise_data = noise_data
