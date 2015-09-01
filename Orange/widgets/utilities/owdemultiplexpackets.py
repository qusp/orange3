# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import DemultiplexPackets


class OWDemultiplexPackets(widget.OWWidget):
    name = "Demultiplex Packets"
    description = "Demultiplex packets from a dict of packets into multiple output packets."
    author = "Christian Kothe"
    icon = "icons/DemultiplexPackets.svg"
    priority = 6
    category = "Utilities"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': 0},
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

    want_main_area = False

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
        super().__init__()

        # Construct node instance and set default properties.
        self.node = DemultiplexPackets()
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

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.name0_control = gui.lineEdit(box, self, 'name0', 'Name0:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name0'))
        self.name1_control = gui.lineEdit(box, self, 'name1', 'Name1:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name1'))
        self.name2_control = gui.lineEdit(box, self, 'name2', 'Name2:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name2'))
        self.name3_control = gui.lineEdit(box, self, 'name3', 'Name3:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name3'))
        self.name4_control = gui.lineEdit(box, self, 'name4', 'Name4:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name4'))
        self.name5_control = gui.lineEdit(box, self, 'name5', 'Name5:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name5'))
        self.name6_control = gui.lineEdit(box, self, 'name6', 'Name6:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name6'))
        self.name7_control = gui.lineEdit(box, self, 'name7', 'Name7:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name7'))
        self.name8_control = gui.lineEdit(box, self, 'name8', 'Name8:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name8'))
        self.name9_control = gui.lineEdit(box, self, 'name9', 'Name9:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('name9'))
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

        # Set minimum width (in pixels).
        self.setMinimumWidth(480)

    def get_property_names(self):
        return list(self.node.ports(editable=True).keys())

    def get_property_control(self, name):
        return getattr(self, '{}_control'.format(name))

    def enable_property_control(self, name):
        self.get_property_control(name).setDisabled(False)

    def disable_property_control(self, name):
        self.get_property_control(name).setDisabled(True)

    def enable_property_controls(self, names=None):
        for name in (names or self.get_property_names()):
            self.enable_property_control(name)

    def disable_property_controls(self, names=None):
        for name in (names or self.get_property_names()):
            self.disable_property_control(name)

    def reset_default_properties(self, names=None):
        node = DemultiplexPackets()

        for name in (names or self.get_property_names()):
            setattr(self.node, name, getattr(node, name))
            # Synchronize property changes back to the GUI.
            super().__setattr__(name, getattr(self.node, name))

    def property_changed(self, name):
        if self.last_error_caused_by and self.last_error_caused_by != name:
            return

        try:
            if self.node.port(name).value_type in (bool, str):
                value = getattr(self, name)
            else:
                # Evaluate string as pure Python code.
                value = eval(getattr(self, name))

            setattr(self.node, name, value)
            # Synchronize property changes back to the GUI.
            super().__setattr__(name, getattr(self.node, name))

            if self.last_error_caused_by:
                self.last_error_caused_by = ''
                self.error()

            self.enable_property_controls()
            self.reset_button.setDisabled(False)
        except Exception as e:
            self.disable_property_controls()
            self.reset_button.setDisabled(True)
            self.enable_property_control(name)

            if not self.last_error_caused_by:
                self.last_error_caused_by = name

            self.error(text=str(e))

    def set_update(self, update):
        self.node.update = update

    def set_indict(self, indict):
        self.node.indict = indict


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWDemultiplexPackets()
    ow.show()
    app.exec_()