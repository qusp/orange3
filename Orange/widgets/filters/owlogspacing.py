# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import LogSpacing


class OWLogSpacing(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Log Spacing"
    description = "Sub-sample an axis with log-spacing."
    author = "Christian Kothe"
    icon = "icons/LogSpacing.svg"
    priority = 9
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
    axis = Setting(None)
    points = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(LogSpacing())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('points', self.node.points)
        else:
            self.node.axis = self.axis
            self.node.points = self.points

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('frequency', 'instance', 'feature', 'space', 'axis', 'lag', 'statistic', 'time'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to prune. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency', 'instance', 'feature', ...).")
        self.points_control = gui.lineEdit(box, self, 'points', label='Points:', orientation='horizontal', callback=lambda: self.property_changed('points'), tooltip="Number of sampling points.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
