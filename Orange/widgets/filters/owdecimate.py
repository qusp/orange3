# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import Decimate


class OWDecimate(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Decimate"
    description = "Decimate the given signal by aninteger factor; does no anti-aliasing."
    author = "Christian Kothe"
    icon = "icons/Decimate.svg"
    priority = 2
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
    factor = Setting(None)
    axis = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Decimate())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('factor', self.node.factor)
            super().__setattr__('axis', self.node.axis)
        else:
            self.node.factor = self.factor
            self.node.axis = self.axis

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.factor_control = gui.lineEdit(box, self, 'factor', label='Factor:', orientation='horizontal', callback=lambda: self.property_changed('factor'), tooltip="Decimation factor.")
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('statistic', 'space', 'axis', 'instance', 'time', 'lag', 'feature', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to apply filter to. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency'). Default: 'time'.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
