# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import LASSORegression


class OWLASSORegression(widget.OWWidget):
    name = 'LASSO Regression'
    description = 'Implements the LASSO regression method (a form of sparse linear regression). See also sklearn.linear_model.LassoCV.'
    author = 'Christian Kothe'
    icon = 'icons/LASSORegression.svg'
    priority = 5
    category = 'Machine_Learning'

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

    num_alphas = Setting(None)
    num_folds = Setting(None)
    max_iter = Setting(None)
    tolerance = Setting(None)
    num_jobs = Setting(None)
    verbosity = Setting(None)
    include_bias = Setting(None)
    normalize_features = Setting(None)
    min_alpha = Setting(None)
    alphas = Setting(None)
    selection = Setting(None)
    positivity_constraint = Setting(None)
    precompute = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = LASSORegression()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_alphas', self.node.num_alphas)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('normalize_features', self.node.normalize_features)
            super().__setattr__('min_alpha', self.node.min_alpha)
            super().__setattr__('alphas', self.node.alphas)
            super().__setattr__('selection', self.node.selection)
            super().__setattr__('positivity_constraint', self.node.positivity_constraint)
            super().__setattr__('precompute', self.node.precompute)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.num_alphas = self.num_alphas
            self.node.num_folds = self.num_folds
            self.node.max_iter = self.max_iter
            self.node.tolerance = self.tolerance
            self.node.num_jobs = self.num_jobs
            self.node.verbosity = self.verbosity
            self.node.include_bias = self.include_bias
            self.node.normalize_features = self.normalize_features
            self.node.min_alpha = self.min_alpha
            self.node.alphas = self.alphas
            self.node.selection = self.selection
            self.node.positivity_constraint = self.positivity_constraint
            self.node.precompute = self.precompute
            self.node.random_seed = self.random_seed

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_alphas_control = gui.lineEdit(box, self, 'num_alphas', 'Num alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_alphas'))
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'))
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'))
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'))
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', 'Normalize features', callback=lambda: self.property_changed('normalize_features'))
        self.min_alpha_control = gui.lineEdit(box, self, 'min_alpha', 'Min alpha:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('min_alpha'))
        self.alphas_control = gui.lineEdit(box, self, 'alphas', 'Alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alphas'))
        self.selection_control = gui.lineEdit(box, self, 'selection', 'Selection:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('selection'))
        self.positivity_constraint_control = gui.checkBox(box, self, 'positivity_constraint', 'Positivity constraint', callback=lambda: self.property_changed('positivity_constraint'))
        self.precompute_control = gui.lineEdit(box, self, 'precompute', 'Precompute:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('precompute'))
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
        node = LASSORegression()

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
    ow = OWLASSORegression()
    ow.show()
    app.exec_()