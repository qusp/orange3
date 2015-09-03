# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import InfomaxICA


class OWInfomaxICA(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Infomax Independent Component Analysis"
    description = "Transform the given signal into independent component space."
    author = "Christian Kothe"
    icon = "icons/InfomaxICA.svg"
    priority = 8
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
    max_iters = Setting(None)
    verbosity = Setting(None)
    learning_rate = Setting(None)
    calib_seconds = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(InfomaxICA())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('max_iters', self.node.max_iters)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('learning_rate', self.node.learning_rate)
            super().__setattr__('calib_seconds', self.node.calib_seconds)
        else:
            self.node.max_iters = self.max_iters
            self.node.verbosity = self.verbosity
            self.node.learning_rate = self.learning_rate
            self.node.calib_seconds = self.calib_seconds

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.max_iters_control = gui.lineEdit(box, self, 'max_iters', 'Max iters:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iters'), tooltip="Maximum number of iterations.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.learning_rate_control = gui.lineEdit(box, self, 'learning_rate', 'Learning rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('learning_rate'), tooltip="Learning rate. Reduce if the algorithm diverges.")
        self.calib_seconds_control = gui.lineEdit(box, self, 'calib_seconds', 'Calib seconds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('calib_seconds'), tooltip="Data length for calibration. In seconds. Note that for many channels, ICA needs quite a bit of calibration data.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
