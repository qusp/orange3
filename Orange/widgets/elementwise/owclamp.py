# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.elementwise import Clamp


class OWClamp(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Clamp"
    description = "Clamp the given values between a minimum and a maximum.."
    author = "Christian Kothe"
    icon = "icons/Clamp.svg"
    priority = 1
    category = "Elementwise"

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
    min = Setting(None)
    max = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Clamp())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('min', self.node.min)
            super().__setattr__('max', self.node.max)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.min = self.min
            self.node.max = self.max
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.min_control = gui.lineEdit(box, self, 'min', 'Min:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('min'), tooltip="Minimum value.")
        self.max_control = gui.lineEdit(box, self, 'max', 'Max:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max'), tooltip="Maximum value.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any numeric chunk data will be processed.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
