# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import XDAWN


class OWXDAWN(cpewidget.CPEWidget):

    # Node meta-data.
    name = "xDAWN Spatial Filter"
    description = "Enhance evoked EEG responses using the xDAWN algorithm."
    author = "Christian Kothe"
    icon = "icons/XDAWN.svg"
    priority = 13
    category = "Feature_Extraction"

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
    erp_duration = Setting(None)
    num_components = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(XDAWN())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('erp_duration', self.node.erp_duration)
            super().__setattr__('num_components', self.node.num_components)
        else:
            self.node.erp_duration = self.erp_duration
            self.node.num_components = self.num_components

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.erp_duration_control = gui.lineEdit(box, self, 'erp_duration', 'Erp duration:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('erp_duration'), tooltip="Duration of the stimulus-evoked activity, in seconds.")
        self.num_components_control = gui.lineEdit(box, self, 'num_components', 'Num components:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_components'), tooltip="Number of xDAWN components to retain.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
