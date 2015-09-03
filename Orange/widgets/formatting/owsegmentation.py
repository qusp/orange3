# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.formatting import Segmentation


class OWSegmentation(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Segmentation"
    description = "Extract segments from a continuous time series."
    author = "Christian Kothe"
    icon = "icons/Segmentation.svg"
    priority = 1
    category = "Formatting"

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
    time_bounds = Setting(None)
    online_epoching = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Segmentation())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('time_bounds', self.node.time_bounds)
            super().__setattr__('online_epoching', self.node.online_epoching)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.time_bounds = self.time_bounds
            self.node.online_epoching = self.online_epoching
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.time_bounds_control = gui.lineEdit(box, self, 'time_bounds', label='Time bounds:', orientation='horizontal', callback=lambda: self.property_changed('time_bounds'), tooltip="Time window relative to markers. For each target marker, a segment will be extracted that lies relative to the marker.")
        self.online_epoching_control = gui.comboBox(box, self, 'online_epoching', label='Online epoching:', items=('marker-locked', 'sliding'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('online_epoching'), tooltip="How to extract segments when streaming. When using 'marker-locked', windows are extracted relative to the target markers; when using 'sliding', a single sliding window is extracted that lies at the end of the data.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Segment signal chunks. If unset, any numeric chunk with a time axis will be segmented. Note that marker chunks are generally segmented, too.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
