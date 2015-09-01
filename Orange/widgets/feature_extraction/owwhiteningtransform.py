# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import WhiteningTransform


class OWWhiteningTransform(widget.OWWidget):
    name = "Whitening Transform"
    description = "Whiten (decorrelate and normalize) the given data without rotation."
    author = "Christian Kothe"
    icon = "icons/WhiteningTransform.svg"
    priority = 12
    category = "Feature_Extraction"

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

    shrinkage = Setting(None)
    center = Setting(None)
    decorrelate = Setting(None)
    retain_axes = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = WhiteningTransform()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('shrinkage', self.node.shrinkage)
            super().__setattr__('center', self.node.center)
            super().__setattr__('decorrelate', self.node.decorrelate)
            super().__setattr__('retain_axes', self.node.retain_axes)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
        else:
            self.node.shrinkage = self.shrinkage
            self.node.center = self.center
            self.node.decorrelate = self.decorrelate
            self.node.retain_axes = self.retain_axes
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', 'Shrinkage:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('shrinkage'))
        self.center_control = gui.checkBox(box, self, 'center', 'Center', callback=lambda: self.property_changed('center'))
        self.decorrelate_control = gui.checkBox(box, self, 'decorrelate', 'Decorrelate', callback=lambda: self.property_changed('decorrelate'))
        self.retain_axes_control = gui.checkBox(box, self, 'retain_axes', 'Retain axes', callback=lambda: self.property_changed('retain_axes'))
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'))
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', 'Domain axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('domain_axes'))
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', 'Aggregate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('aggregate_axes'))
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', 'Separate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('separate_axes'))
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
        node = WhiteningTransform()

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
    ow = OWWhiteningTransform()
    ow.show()
    app.exec_()