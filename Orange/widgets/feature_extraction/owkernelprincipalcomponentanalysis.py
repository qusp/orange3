# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import KernelPrincipalComponentAnalysis


class OWKernelPrincipalComponentAnalysis(widget.OWWidget):
    name = "Kernel Principal Component Analysis"
    description = "Non-linear dimensionality reduction using Kernel Principal Component Analysis."
    author = "Christian Kothe"
    icon = "icons/KernelPrincipalComponentAnalysis.svg"
    priority = 5
    category = "Feature_Extraction"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    num_components = Setting(None)
    kernel = Setting(None)
    poly_degree = Setting(None)
    gamma = Setting(None)
    coef0 = Setting(None)
    remove_zero_eig = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = KernelPrincipalComponentAnalysis()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_components', self.node.num_components)
            super().__setattr__('kernel', self.node.kernel)
            super().__setattr__('poly_degree', self.node.poly_degree)
            super().__setattr__('gamma', self.node.gamma)
            super().__setattr__('coef0', self.node.coef0)
            super().__setattr__('remove_zero_eig', self.node.remove_zero_eig)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
        else:
            self.node.num_components = self.num_components
            self.node.kernel = self.kernel
            self.node.poly_degree = self.poly_degree
            self.node.gamma = self.gamma
            self.node.coef0 = self.coef0
            self.node.remove_zero_eig = self.remove_zero_eig
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_components_control = gui.lineEdit(box, self, 'num_components', 'Num components:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_components'))
        self.kernel_control = gui.lineEdit(box, self, 'kernel', 'Kernel:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('kernel'))
        self.poly_degree_control = gui.lineEdit(box, self, 'poly_degree', 'Poly degree:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('poly_degree'))
        self.gamma_control = gui.lineEdit(box, self, 'gamma', 'Gamma:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('gamma'))
        self.coef0_control = gui.lineEdit(box, self, 'coef0', 'Coef0:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('coef0'))
        self.remove_zero_eig_control = gui.checkBox(box, self, 'remove_zero_eig', 'Remove zero eig', callback=lambda: self.property_changed('remove_zero_eig'))
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
        node = KernelPrincipalComponentAnalysis()

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
    ow = OWKernelPrincipalComponentAnalysis()
    ow.show()
    app.exec_()