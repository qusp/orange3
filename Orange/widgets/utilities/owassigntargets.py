# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import AssignTargets


class OWAssignTargets(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Assign Targets"
    description = "Assign target values to a subset of events."
    author = "Christian Kothe"
    icon = "icons/AssignTargets.svg"
    priority = 3
    category = "Utilities"

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
    mapping = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(AssignTargets())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('mapping', self.node.mapping)
        else:
            self.node.mapping = self.mapping

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.mapping_control = gui.lineEdit(box, self, 'mapping', label='Mapping:', orientation='horizontal', callback=lambda: self.property_changed('mapping'), tooltip="Target value mapping. A map from marker payload (label) to numeric target value.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
