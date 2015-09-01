# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import ASRFilter


class OWASRFilter(widget.OWWidget):
    name = "Artifact Removal"
    description = "This is used to clean a multi-channel signal using an advanced method."
    author = "Christian Kothe and Alejandro Ojeda"
    icon = "icons/ASRFilter.svg"
    priority = 1
    category = "Filters"

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

    cutoff = Setting(None)
    block_size = Setting(None)
    b = Setting(None)
    a = Setting(None)
    window_len = Setting(None)
    lookahead = Setting(None)
    window_overlap = Setting(None)
    max_dropout_fraction = Setting(None)
    min_clean_fraction = Setting(None)
    step_size = Setting(None)
    max_dims = Setting(None)
    max_mem = Setting(None)
    calib_seconds = Setting(None)
    discard_chunk_seconds = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = ASRFilter()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('cutoff', self.node.cutoff)
            super().__setattr__('block_size', self.node.block_size)
            super().__setattr__('b', self.node.b)
            super().__setattr__('a', self.node.a)
            super().__setattr__('window_len', self.node.window_len)
            super().__setattr__('lookahead', self.node.lookahead)
            super().__setattr__('window_overlap', self.node.window_overlap)
            super().__setattr__('max_dropout_fraction', self.node.max_dropout_fraction)
            super().__setattr__('min_clean_fraction', self.node.min_clean_fraction)
            super().__setattr__('step_size', self.node.step_size)
            super().__setattr__('max_dims', self.node.max_dims)
            super().__setattr__('max_mem', self.node.max_mem)
            super().__setattr__('calib_seconds', self.node.calib_seconds)
            super().__setattr__('discard_chunk_seconds', self.node.discard_chunk_seconds)
        else:
            self.node.cutoff = self.cutoff
            self.node.block_size = self.block_size
            self.node.b = self.b
            self.node.a = self.a
            self.node.window_len = self.window_len
            self.node.lookahead = self.lookahead
            self.node.window_overlap = self.window_overlap
            self.node.max_dropout_fraction = self.max_dropout_fraction
            self.node.min_clean_fraction = self.min_clean_fraction
            self.node.step_size = self.step_size
            self.node.max_dims = self.max_dims
            self.node.max_mem = self.max_mem
            self.node.calib_seconds = self.calib_seconds
            self.node.discard_chunk_seconds = self.discard_chunk_seconds

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.cutoff_control = gui.lineEdit(box, self, 'cutoff', 'Cutoff:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('cutoff'))
        self.block_size_control = gui.lineEdit(box, self, 'block_size', 'Block size:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('block_size'))
        self.b_control = gui.lineEdit(box, self, 'b', 'B:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('b'))
        self.a_control = gui.lineEdit(box, self, 'a', 'A:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('a'))
        self.window_len_control = gui.lineEdit(box, self, 'window_len', 'Window len:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window_len'))
        self.lookahead_control = gui.lineEdit(box, self, 'lookahead', 'Lookahead:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('lookahead'))
        self.window_overlap_control = gui.lineEdit(box, self, 'window_overlap', 'Window overlap:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window_overlap'))
        self.max_dropout_fraction_control = gui.lineEdit(box, self, 'max_dropout_fraction', 'Max dropout fraction:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_dropout_fraction'))
        self.min_clean_fraction_control = gui.lineEdit(box, self, 'min_clean_fraction', 'Min clean fraction:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('min_clean_fraction'))
        self.step_size_control = gui.lineEdit(box, self, 'step_size', 'Step size:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('step_size'))
        self.max_dims_control = gui.lineEdit(box, self, 'max_dims', 'Max dims:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_dims'))
        self.max_mem_control = gui.lineEdit(box, self, 'max_mem', 'Max mem:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_mem'))
        self.calib_seconds_control = gui.lineEdit(box, self, 'calib_seconds', 'Calib seconds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('calib_seconds'))
        self.discard_chunk_seconds_control = gui.lineEdit(box, self, 'discard_chunk_seconds', 'Discard chunk seconds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('discard_chunk_seconds'))
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
        node = ASRFilter()

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
    ow = OWASRFilter()
    ow.show()
    app.exec_()