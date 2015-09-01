# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.general import FoldIntoAxis


class OWFoldIntoAxis(widget.OWWidget):
    name = 'Fold Into Axis'
    description = '"Fold an axis into another axis. The target axis must have per-element names (e.g., space, feature). This will generate an elongated axis that has new names of the form OldName-1, OldName-2, OldName-3, etc.'
    author = 'Christian Kothe'
    icon = 'icons/FoldIntoAxis.svg'
    priority = 6
    category = 'General'

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    src_axis = Setting(None)
    dst_axis = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = FoldIntoAxis()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('src_axis', self.node.src_axis)
            super().__setattr__('dst_axis', self.node.dst_axis)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.src_axis = self.src_axis
            self.node.dst_axis = self.dst_axis
            self.node.only_signals = self.only_signals

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.src_axis_control = gui.lineEdit(box, self, 'src_axis', 'Src axis:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('src_axis'))
        self.dst_axis_control = gui.lineEdit(box, self, 'dst_axis', 'Dst axis:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('dst_axis'))
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
        node = FoldIntoAxis()

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

    def set_data(self, data):
        self.node.data = data


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWFoldIntoAxis()
    ow.show()
    app.exec_()