# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.feature_extraction import NonNegativeMatrixFactorization


class OWNonNegativeMatrixFactorization(widget.OWWidget):
    name = 'Non-Negative Matrix Factorization'
    description = 'Perform non-negative matrix factorization.'
    author = 'Christian Kothe'
    icon = 'icons/NonNegativeMatrixFactorization.svg'
    priority = 6
    category = 'Feature_Extraction'

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

    num_components = Setting(None)
    max_iter = Setting(None)
    max_iter_nls = Setting(None)
    sparseness = Setting(None)
    tolerance = Setting(None)
    beta = Setting(None)
    eta = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)
    init = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = NonNegativeMatrixFactorization()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_components', self.node.num_components)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('max_iter_nls', self.node.max_iter_nls)
            super().__setattr__('sparseness', self.node.sparseness)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('beta', self.node.beta)
            super().__setattr__('eta', self.node.eta)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
            super().__setattr__('init', self.node.init)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.num_components = self.num_components
            self.node.max_iter = self.max_iter
            self.node.max_iter_nls = self.max_iter_nls
            self.node.sparseness = self.sparseness
            self.node.tolerance = self.tolerance
            self.node.beta = self.beta
            self.node.eta = self.eta
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes
            self.node.init = self.init
            self.node.random_seed = self.random_seed

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_components_control = gui.lineEdit(box, self, 'num_components', 'Num components:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_components'))
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.max_iter_nls_control = gui.lineEdit(box, self, 'max_iter_nls', 'Max iter nls:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter_nls'))
        self.sparseness_control = gui.lineEdit(box, self, 'sparseness', 'Sparseness:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('sparseness'))
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'))
        self.beta_control = gui.lineEdit(box, self, 'beta', 'Beta:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('beta'))
        self.eta_control = gui.lineEdit(box, self, 'eta', 'Eta:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('eta'))
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'))
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', 'Domain axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('domain_axes'))
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', 'Aggregate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('aggregate_axes'))
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', 'Separate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('separate_axes'))
        self.init_control = gui.lineEdit(box, self, 'init', 'Init:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('init'))
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'))
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
        node = NonNegativeMatrixFactorization()

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
    ow = OWNonNegativeMatrixFactorization()
    ow.show()
    app.exec_()