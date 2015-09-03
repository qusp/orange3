# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import EnsureIdentical


class OWEnsureIdentical(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Ensure Identical Signals"
    description = "Ensure that the two input signals have identical numeric data (and optionally meta-data as well)"
    author = "Christian Kothe"
    icon = "icons/EnsureIdentical.svg"
    priority = 8
    category = "Utilities"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data1', 'type': builtins.object, 'handler': 'set_data1', 'flags': 0},
        {'name': 'Data2', 'type': builtins.object, 'handler': 'set_data2', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
    ]

    # Configuration properties.
    check_metadata = Setting(None)
    tolerance = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(EnsureIdentical())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('check_metadata', self.node.check_metadata)
            super().__setattr__('tolerance', self.node.tolerance)
        else:
            self.node.check_metadata = self.check_metadata
            self.node.tolerance = self.tolerance

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.check_metadata_control = gui.checkBox(box, self, 'check_metadata', label='Check metadata', callback=lambda: self.property_changed('check_metadata'), tooltip="Also check meta-data. If false, only the numeric contents are checked.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', label='Tolerance:', orientation='horizontal', callback=lambda: self.property_changed('tolerance'), tooltip="Numerical tolerance. Relative to the norm of the values.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data1(self, data1):
        self.node.data1 = data1

    def set_data2(self, data2):
        self.node.data2 = data2
