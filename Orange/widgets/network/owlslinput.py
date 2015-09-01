# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.network import LSLInput


class OWLSLInput(widget.OWWidget):
    name = "LSL Input"
    description = "Receive data from LSL"
    author = "Christian Kothe"
    icon = "icons/LSLInput.svg"
    priority = 1
    category = "Network"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    query = Setting(None)
    marker_query = Setting(None)
    max_buflen = Setting(None)
    max_chunklen = Setting(None)
    max_blocklen = Setting(None)
    recover = Setting(None)
    channel_names = Setting(None)
    nominal_rate = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = LSLInput()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('query', self.node.query)
            super().__setattr__('marker_query', self.node.marker_query)
            super().__setattr__('max_buflen', self.node.max_buflen)
            super().__setattr__('max_chunklen', self.node.max_chunklen)
            super().__setattr__('max_blocklen', self.node.max_blocklen)
            super().__setattr__('recover', self.node.recover)
            super().__setattr__('channel_names', self.node.channel_names)
            super().__setattr__('nominal_rate', self.node.nominal_rate)
        else:
            self.node.query = self.query
            self.node.marker_query = self.marker_query
            self.node.max_buflen = self.max_buflen
            self.node.max_chunklen = self.max_chunklen
            self.node.max_blocklen = self.max_blocklen
            self.node.recover = self.recover
            self.node.channel_names = self.channel_names
            self.node.nominal_rate = self.nominal_rate

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.query_control = gui.lineEdit(box, self, 'query', 'Query:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('query'))
        self.marker_query_control = gui.lineEdit(box, self, 'marker_query', 'Marker query:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('marker_query'))
        self.max_buflen_control = gui.lineEdit(box, self, 'max_buflen', 'Max buflen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_buflen'))
        self.max_chunklen_control = gui.lineEdit(box, self, 'max_chunklen', 'Max chunklen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_chunklen'))
        self.max_blocklen_control = gui.lineEdit(box, self, 'max_blocklen', 'Max blocklen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_blocklen'))
        self.recover_control = gui.checkBox(box, self, 'recover', 'Recover', callback=lambda: self.property_changed('recover'))
        self.channel_names_control = gui.lineEdit(box, self, 'channel_names', 'Channel names:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('channel_names'))
        self.nominal_rate_control = gui.lineEdit(box, self, 'nominal_rate', 'Nominal rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('nominal_rate'))
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
        node = LSLInput()

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWLSLInput()
    ow.show()
    app.exec_()