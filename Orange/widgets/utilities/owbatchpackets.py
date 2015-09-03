# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import BatchPackets


class OWBatchPackets(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Merge Successive Packets"
    description = "Merges successive packets to maintain real-time rates. Normally, the pipeline is driven by input plugins that output all data since the last update, which naturally increases the chunk size if necessary to maintain real-time rates. However, when the pipeline is driven with a fixed chunk size that is too small for real time, this node can be inserted to merge successive  chunks (actually packets) in order to achieve real-time behavior."
    author = "Christian Kothe"
    icon = "icons/BatchPackets.svg"
    priority = 4
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
    batching = Setting(None)
    batchsize = Setting(None)
    max_input_lag = Setting(None)
    max_output_lag = Setting(None)
    axis = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(BatchPackets())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('batching', self.node.batching)
            super().__setattr__('batchsize', self.node.batchsize)
            super().__setattr__('max_input_lag', self.node.max_input_lag)
            super().__setattr__('max_output_lag', self.node.max_output_lag)
            super().__setattr__('axis', self.node.axis)
        else:
            self.node.batching = self.batching
            self.node.batchsize = self.batchsize
            self.node.max_input_lag = self.max_input_lag
            self.node.max_output_lag = self.max_output_lag
            self.node.axis = self.axis

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.batching_control = gui.comboBox(box, self, 'batching', label='Batching:', items=['realtime', 'fixed'], sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('batching'), tooltip="Batching mode. If set to 'realtime', then as many packets are merged as necessary to maintain real-time updates. If set to 'fixed', then a fixed number of successive packets (batchsize) are merged.")
        self.batchsize_control = gui.lineEdit(box, self, 'batchsize', label='Batchsize:', orientation='horizontal', callback=lambda: self.property_changed('batchsize'), tooltip="Number of successive packets to merge. Only used if batching is set to 'fixed'.")
        self.max_input_lag_control = gui.lineEdit(box, self, 'max_input_lag', label='Max input lag:', orientation='horizontal', callback=lambda: self.property_changed('max_input_lag'), tooltip="Maximum input packet lag beyond which the system will stash the packet and batch it with the next one (in 'realtime' mode), in seconds.")
        self.max_output_lag_control = gui.lineEdit(box, self, 'max_output_lag', label='Max output lag:', orientation='horizontal', callback=lambda: self.property_changed('max_output_lag'), tooltip="Maximum delay incurred by batching packets, in seconds.")
        self.axis_control = gui.lineEdit(box, self, 'axis', label='Axis:', orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to concatenate along. If set to 'auto', concatenation goes along the instance axis if present, or time axis otherwise.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
