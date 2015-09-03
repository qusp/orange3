# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import MeasureLoss


class OWMeasureLoss(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Measure Loss"
    description = "Measure the loss between predictions and targets."
    author = "Christian Kothe"
    icon = "icons/MeasureLoss.svg"
    priority = 10
    category = "Machine_Learning"

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
    loss_metric = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(MeasureLoss())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('loss_metric', self.node.loss_metric)
        else:
            self.node.loss_metric = self.loss_metric

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.loss_metric_control = gui.comboBox(box, self, 'loss_metric', label='Loss metric:', items=('MCR',), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('loss_metric'), tooltip="Loss metric. MCR stands for mis-classification rate (aka error rate).")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
