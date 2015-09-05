# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import SampleCovariance


class OWSampleCovariance(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Sample Covariance"
    description = "Calculate the covariance between all elements of a given axis; replicates the given axis."
    author = "Christian Kothe"
    icon = "icons/SampleCovariance.svg"
    priority = 10
    category = "General"

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
    shrinkage = Setting(None)
    axis = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SampleCovariance())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('shrinkage', self.node.shrinkage)
            super().__setattr__('axis', self.node.axis)
        else:
            self.node.shrinkage = self.shrinkage
            self.node.axis = self.axis

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', label='Shrinkage:', orientation='horizontal', callback=lambda: self.property_changed('shrinkage'), tooltip="Amount of shrinkage to apply to covariance estimate.  This is a regularization method that protects against degenerate matrices.")
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('lag', 'time', 'feature', 'space', 'axis', 'statistic', 'frequency', 'instance'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to take covariance of. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency', 'instance', 'feature', ...).")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
