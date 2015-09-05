# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import ConcatInputs


class OWConcatInputs(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Concatenate Inputs"
    description = "Concatenate the given input packets along a new or existing axis."
    author = "Christian Kothe"
    icon = "icons/ConcatInputs.svg"
    priority = 3
    category = "General"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data1', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data1', 'flags': 0},
        {'name': 'Data2', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data2', 'flags': 0},
        {'name': 'Data3', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data3', 'flags': 0},
        {'name': 'Data4', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data4', 'flags': 0},
        {'name': 'Data5', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data5', 'flags': 0},
        {'name': 'Data6', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data6', 'flags': 0},
        {'name': 'Data7', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data7', 'flags': 0},
        {'name': 'Data8', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data8', 'flags': 0},
        {'name': 'Data9', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data9', 'flags': 0},
        {'name': 'Data10', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data10', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Outdata', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    axis = Setting(None)
    create_new = Setting(None)
    properties = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ConcatInputs())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('create_new', self.node.create_new)
            super().__setattr__('properties', self.node.properties)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.axis = self.axis
            self.node.create_new = self.create_new
            self.node.properties = self.properties
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('statistic', 'space', 'axis', 'instance', 'time', 'lag', 'feature', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="New axis type to fold into.")
        self.create_new_control = gui.checkBox(box, self, 'create_new', label='Create new', callback=lambda: self.property_changed('create_new'), tooltip="Whether to create a new axis.")
        self.properties_control = gui.lineEdit(box, self, 'properties', label='Properties:', orientation='horizontal', callback=lambda: self.property_changed('properties'), tooltip="Values for the primary property of the axis, e.g., list of channel names if the axis is 'space'. Only applies when creating a new axis.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Concatenate only the signal chunks. If true, the non-signal chunks will be taken from the first input data port.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data1(self, data1):
        self.node.data1 = data1

    def set_data2(self, data2):
        self.node.data2 = data2

    def set_data3(self, data3):
        self.node.data3 = data3

    def set_data4(self, data4):
        self.node.data4 = data4

    def set_data5(self, data5):
        self.node.data5 = data5

    def set_data6(self, data6):
        self.node.data6 = data6

    def set_data7(self, data7):
        self.node.data7 = data7

    def set_data8(self, data8):
        self.node.data8 = data8

    def set_data9(self, data9):
        self.node.data9 = data9

    def set_data10(self, data10):
        self.node.data10 = data10
