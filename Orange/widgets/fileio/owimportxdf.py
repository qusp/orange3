# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.fileio import ImportXDF


class OWImportXDF(widget.OWWidget):
    name = 'Import XDF'
    description = 'Load data from a .xdf file'
    author = 'Christian Kothe'
    icon = 'icons/ImportXDF.svg'
    priority = 2
    category = 'Fileio'

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    filename = Setting(None)
    verbose = Setting(None)
    retain_streams = Setting(None)
    handle_clock_sync = Setting(None)
    handle_jitter_removal = Setting(None)
    handle_clock_resets = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = ImportXDF()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('filename', self.node.filename)
            super().__setattr__('verbose', self.node.verbose)
            super().__setattr__('retain_streams', self.node.retain_streams)
            super().__setattr__('handle_clock_sync', self.node.handle_clock_sync)
            super().__setattr__('handle_jitter_removal', self.node.handle_jitter_removal)
            super().__setattr__('handle_clock_resets', self.node.handle_clock_resets)
        else:
            self.node.filename = self.filename
            self.node.verbose = self.verbose
            self.node.retain_streams = self.retain_streams
            self.node.handle_clock_sync = self.handle_clock_sync
            self.node.handle_jitter_removal = self.handle_jitter_removal
            self.node.handle_clock_resets = self.handle_clock_resets

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.filename_control = gui.lineEdit(box, self, 'filename', 'Filename:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('filename'))
        self.verbose_control = gui.checkBox(box, self, 'verbose', 'Verbose', callback=lambda: self.property_changed('verbose'))
        self.retain_streams_control = gui.lineEdit(box, self, 'retain_streams', 'Retain streams:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('retain_streams'))
        self.handle_clock_sync_control = gui.checkBox(box, self, 'handle_clock_sync', 'Handle clock sync', callback=lambda: self.property_changed('handle_clock_sync'))
        self.handle_jitter_removal_control = gui.checkBox(box, self, 'handle_jitter_removal', 'Handle jitter removal', callback=lambda: self.property_changed('handle_jitter_removal'))
        self.handle_clock_resets_control = gui.checkBox(box, self, 'handle_clock_resets', 'Handle clock resets', callback=lambda: self.property_changed('handle_clock_resets'))
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
        node = ImportXDF()

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
    ow = OWImportXDF()
    ow.show()
    app.exec_()