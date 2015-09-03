# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.elementwise import Sigmoid


class OWSigmoid(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Sigmoid"
    description = "Sigmoidal transform of numeric values."
    author = "Christian Kothe"
    icon = "icons/Sigmoid.svg"
    priority = 15
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
    pre_shift = Setting(None)
    pre_scale = Setting(None)
    post_scale = Setting(None)
    post_shift = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Sigmoid())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('pre_shift', self.node.pre_shift)
            super().__setattr__('pre_scale', self.node.pre_scale)
            super().__setattr__('post_scale', self.node.post_scale)
            super().__setattr__('post_shift', self.node.post_shift)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.pre_shift = self.pre_shift
            self.node.pre_scale = self.pre_scale
            self.node.post_scale = self.post_scale
            self.node.post_shift = self.post_shift
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.pre_shift_control = gui.lineEdit(box, self, 'pre_shift', label='Pre shift:', orientation='horizontal', callback=lambda: self.property_changed('pre_shift'), tooltip="Shift prior to sigmoid transform.")
        self.pre_scale_control = gui.lineEdit(box, self, 'pre_scale', label='Pre scale:', orientation='horizontal', callback=lambda: self.property_changed('pre_scale'), tooltip="Scaling prior to sigmoid transform.")
        self.post_scale_control = gui.lineEdit(box, self, 'post_scale', label='Post scale:', orientation='horizontal', callback=lambda: self.property_changed('post_scale'), tooltip="Scaling after sigmoid transform.")
        self.post_shift_control = gui.lineEdit(box, self, 'post_shift', label='Post shift:', orientation='horizontal', callback=lambda: self.property_changed('post_shift'), tooltip="Shift after sigmoid transform.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any numeric chunk data will be processed.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
