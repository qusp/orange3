# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.custom import ConcentrationIndex


class OWConcentrationIndex(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Concentration Index"
    description = "Computes a concentration index as defined in http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4042686."
    author = "Alejandro Ojeda (alejandro.ojeda@syntrogi.com)"
    icon = "icons/ConcentrationIndex.svg"
    priority = 1
    category = "Custom"

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
    frequencies_num = Setting(None)
    frequencies_den = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ConcentrationIndex())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('frequencies_num', self.node.frequencies_num)
            super().__setattr__('frequencies_den', self.node.frequencies_den)
        else:
            self.node.frequencies_num = self.frequencies_num
            self.node.frequencies_den = self.frequencies_den

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.frequencies_num_control = gui.lineEdit(box, self, 'frequencies_num', 'Frequencies num:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('frequencies_num'), tooltip="Frequency bands to average over in the numerator. Default: Beta band.")
        self.frequencies_den_control = gui.lineEdit(box, self, 'frequencies_den', 'Frequencies den:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('frequencies_den'), tooltip="Frequency bands to average over in the numerator. Default: Theta and Alpha bands.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
