# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import Rereferencing


class OWRereferencing(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Re-referencing"
    description = "Re-reference the data across a given axis (usually across \'space\')."
    author = "Christian Kothe"
    icon = "icons/Rereferencing.svg"
    priority = 13
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
    estimator = Setting(None)
    reference_range = Setting(None)
    reference_unit = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Rereferencing())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('estimator', self.node.estimator)
            super().__setattr__('reference_range', self.node.reference_range)
            super().__setattr__('reference_unit', self.node.reference_unit)
        else:
            self.node.axis = self.axis
            self.node.estimator = self.estimator
            self.node.reference_range = self.reference_range
            self.node.reference_unit = self.reference_unit

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('frequency', 'instance', 'feature', 'space', 'axis', 'lag', 'statistic', 'time'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis across which to re-reference. This is usually 'space'.")
        self.estimator_control = gui.comboBox(box, self, 'estimator', label='Estimator:', items=('mean', 'median'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('estimator'), tooltip="Estimator to use. Mean is the standard choice, median is a robust alternative (tolerates bad channels).")
        self.reference_range_control = gui.lineEdit(box, self, 'reference_range', label='Reference range:', orientation='horizontal', callback=lambda: self.property_changed('reference_range'), tooltip="Data range to use as reference. This is typically a channel range, e.g. ':' or ['TP8', 'TP9'] or ['Chn1':'Chn10'].")
        self.reference_unit_control = gui.comboBox(box, self, 'reference_unit', label='Reference unit:', items=('sec', 'names', 'units', 'samples', 'sampling_distrib', 'property', 'parameter_type', 'data', 'Hz', 'seconds', 'fraction', 'indices', 'error_distrib'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('reference_unit'), tooltip="Selection unit. Depending on the axis, different units are applicable.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
