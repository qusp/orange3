# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import FiniteDifferences


class OWFiniteDifferences(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Finite Differences"
    description = "Calculate finite differences along a given axis, up to a given order."
    author = "Christian Kothe"
    icon = "icons/FiniteDifferences.svg"
    priority = 5
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
    axis = Setting(None)
    order = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(FiniteDifferences())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('order', self.node.order)
        else:
            self.node.axis = self.axis
            self.node.order = self.order

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('time', 'instance', 'space', 'feature', 'frequency', 'statistic', 'axis', 'lag'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to prune. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency', 'instance', 'feature', ...). ")
        self.order_control = gui.lineEdit(box, self, 'order', label='Order:', orientation='horizontal', callback=lambda: self.property_changed('order'), tooltip="Differencing order.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
