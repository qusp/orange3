# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import DemultiplexPackets


class OWDemultiplexPackets(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Demultiplex Packets"
    description = "Demultiplex packets from a dict of packets into multiple output packets."
    author = "Christian Kothe"
    icon = "icons/DemultiplexPackets.svg"
    priority = 6
    category = "Utilities"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Indict', 'type': builtins.dict, 'handler': 'set_indict', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Out0', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out1', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out2', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out3', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out4', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out5', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out6', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out7', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out8', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Out9', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    name0 = Setting(None)
    name1 = Setting(None)
    name2 = Setting(None)
    name3 = Setting(None)
    name4 = Setting(None)
    name5 = Setting(None)
    name6 = Setting(None)
    name7 = Setting(None)
    name8 = Setting(None)
    name9 = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(DemultiplexPackets())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('name0', self.node.name0)
            super().__setattr__('name1', self.node.name1)
            super().__setattr__('name2', self.node.name2)
            super().__setattr__('name3', self.node.name3)
            super().__setattr__('name4', self.node.name4)
            super().__setattr__('name5', self.node.name5)
            super().__setattr__('name6', self.node.name6)
            super().__setattr__('name7', self.node.name7)
            super().__setattr__('name8', self.node.name8)
            super().__setattr__('name9', self.node.name9)
        else:
            self.node.name0 = self.name0
            self.node.name1 = self.name1
            self.node.name2 = self.name2
            self.node.name3 = self.name3
            self.node.name4 = self.name4
            self.node.name5 = self.name5
            self.node.name6 = self.name6
            self.node.name7 = self.name7
            self.node.name8 = self.name8
            self.node.name9 = self.name9

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.name0_control = gui.lineEdit(box, self, 'name0', label='Name0:', orientation='horizontal', callback=lambda: self.property_changed('name0'), tooltip="Name 0.")
        self.name1_control = gui.lineEdit(box, self, 'name1', label='Name1:', orientation='horizontal', callback=lambda: self.property_changed('name1'), tooltip="Name 1.")
        self.name2_control = gui.lineEdit(box, self, 'name2', label='Name2:', orientation='horizontal', callback=lambda: self.property_changed('name2'), tooltip="Name 2.")
        self.name3_control = gui.lineEdit(box, self, 'name3', label='Name3:', orientation='horizontal', callback=lambda: self.property_changed('name3'), tooltip="Name 3.")
        self.name4_control = gui.lineEdit(box, self, 'name4', label='Name4:', orientation='horizontal', callback=lambda: self.property_changed('name4'), tooltip="Name 4.")
        self.name5_control = gui.lineEdit(box, self, 'name5', label='Name5:', orientation='horizontal', callback=lambda: self.property_changed('name5'), tooltip="Name 5.")
        self.name6_control = gui.lineEdit(box, self, 'name6', label='Name6:', orientation='horizontal', callback=lambda: self.property_changed('name6'), tooltip="Name 6.")
        self.name7_control = gui.lineEdit(box, self, 'name7', label='Name7:', orientation='horizontal', callback=lambda: self.property_changed('name7'), tooltip="Name 7.")
        self.name8_control = gui.lineEdit(box, self, 'name8', label='Name8:', orientation='horizontal', callback=lambda: self.property_changed('name8'), tooltip="Name 8.")
        self.name9_control = gui.lineEdit(box, self, 'name9', label='Name9:', orientation='horizontal', callback=lambda: self.property_changed('name9'), tooltip="Name 9.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_indict(self, indict):
        self.node.indict = indict
