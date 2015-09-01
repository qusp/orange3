# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.network import LSLOutput


class OWLSLOutput(widget.OWWidget):
    name = "LSL Output"
    description = "Send data to LSL"
    author = "Christian Kothe"
    icon = "icons/LSLOutput.svg"
    priority = 2
    category = "Network"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
    ]

    want_main_area = False

    stream_name = Setting(None)
    stream_type = Setting(None)
    source_id = Setting(None)
    srate = Setting(None)
    chunk_len = Setting(None)
    max_buffered = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = LSLOutput()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('stream_name', self.node.stream_name)
            super().__setattr__('stream_type', self.node.stream_type)
            super().__setattr__('source_id', self.node.source_id)
            super().__setattr__('srate', self.node.srate)
            super().__setattr__('chunk_len', self.node.chunk_len)
            super().__setattr__('max_buffered', self.node.max_buffered)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.stream_name = self.stream_name
            self.node.stream_type = self.stream_type
            self.node.source_id = self.source_id
            self.node.srate = self.srate
            self.node.chunk_len = self.chunk_len
            self.node.max_buffered = self.max_buffered
            self.node.only_signals = self.only_signals

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.stream_name_control = gui.lineEdit(box, self, 'stream_name', 'Stream name:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('stream_name'))
        self.stream_type_control = gui.lineEdit(box, self, 'stream_type', 'Stream type:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('stream_type'))
        self.source_id_control = gui.lineEdit(box, self, 'source_id', 'Source id:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('source_id'))
        self.srate_control = gui.lineEdit(box, self, 'srate', 'Srate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('srate'))
        self.chunk_len_control = gui.lineEdit(box, self, 'chunk_len', 'Chunk len:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('chunk_len'))
        self.max_buffered_control = gui.lineEdit(box, self, 'max_buffered', 'Max buffered:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_buffered'))
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
        node = LSLOutput()

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
    ow = OWLSLOutput()
    ow.show()
    app.exec_()