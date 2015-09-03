# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import Averages


class OWAverages(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Averages"
    description = "Average values in a given axis in one or more windows."
    author = "Christian Kothe"
    icon = "icons/Averages.svg"
    priority = 1
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
    windows = Setting(None)
    unit = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Averages())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('windows', self.node.windows)
            super().__setattr__('unit', self.node.unit)
        else:
            self.node.axis = self.axis
            self.node.windows = self.windows
            self.node.unit = self.unit

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('time', 'instance', 'space', 'feature', 'frequency', 'statistic', 'axis', 'lag'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to average over. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency', 'instance', 'feature', ...).")
        self.windows_control = gui.lineEdit(box, self, 'windows', label='Windows:', orientation='horizontal', callback=lambda: self.property_changed('windows'), tooltip="List of window edges. Each window is given as a tuple of the start and end of the segment. None instead of a numeric value stands for the beginning/end of the whole data range as in Python slices. The last sample in the segment is excluded.")
        self.unit_control = gui.comboBox(box, self, 'unit', label='Unit:', items=('data', 'indices', 'samples', 'error_distrib', 'Hz', 'units', 'parameter_type', 'sampling_distrib', 'names', 'seconds', 'fraction', 'sec', 'property'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('unit'), tooltip="Selection unit. Depending on the axis, different units are applicable.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
