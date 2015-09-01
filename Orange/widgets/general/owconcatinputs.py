# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import ConcatInputs


class OWConcatInputs(widget.OWWidget):
    name = 'Concatenate Inputs'
    description = 'Concatenate the given input packets along a new or existing axis.'
    author = 'Christian Kothe'
    icon = 'icons/ConcatInputs.svg'
    priority = 3
    category = 'General'

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': 0},
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

    want_main_area = False

    axis = Setting(None)
    create_new = Setting(None)
    properties = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = ConcatInputs()
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

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.lineEdit(box, self, 'axis', 'Axis:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('axis'))
        self.create_new_control = gui.checkBox(box, self, 'create_new', 'Create new', callback=lambda: self.property_changed('create_new'))
        self.properties_control = gui.lineEdit(box, self, 'properties', 'Properties:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('properties'))
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'))
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
        node = ConcatInputs()

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWConcatInputs()
    ow.show()
    app.exec_()