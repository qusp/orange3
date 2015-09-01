# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.machine_learning import SparseBayesianRegression


class OWSparseBayesianRegression(widget.OWWidget):
    name = 'Sparse Bayesian Regression'
    description = 'Implements the sparse Bayesian regression (a form of of sparse linear regression). See also sklearn.linear_model.ARDRegression.'
    author = 'Christian Kothe'
    icon = 'icons/SparseBayesianRegression.svg'
    priority = 15
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

    max_iter = Setting(None)
    tolerance = Setting(None)
    verbosity = Setting(None)
    include_bias = Setting(None)
    normalize_features = Setting(None)
    threshold_lambda = Setting(None)
    alpha_shape = Setting(None)
    alpha_rate = Setting(None)
    lambda_shape = Setting(None)
    lambda_rate = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = SparseBayesianRegression()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('normalize_features', self.node.normalize_features)
            super().__setattr__('threshold_lambda', self.node.threshold_lambda)
            super().__setattr__('alpha_shape', self.node.alpha_shape)
            super().__setattr__('alpha_rate', self.node.alpha_rate)
            super().__setattr__('lambda_shape', self.node.lambda_shape)
            super().__setattr__('lambda_rate', self.node.lambda_rate)
        else:
            self.node.max_iter = self.max_iter
            self.node.tolerance = self.tolerance
            self.node.verbosity = self.verbosity
            self.node.include_bias = self.include_bias
            self.node.normalize_features = self.normalize_features
            self.node.threshold_lambda = self.threshold_lambda
            self.node.alpha_shape = self.alpha_shape
            self.node.alpha_rate = self.alpha_rate
            self.node.lambda_shape = self.lambda_shape
            self.node.lambda_rate = self.lambda_rate

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'))
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', 'Normalize features', callback=lambda: self.property_changed('normalize_features'))
        self.threshold_lambda_control = gui.lineEdit(box, self, 'threshold_lambda', 'Threshold lambda:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('threshold_lambda'))
        self.alpha_shape_control = gui.lineEdit(box, self, 'alpha_shape', 'Alpha shape:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alpha_shape'))
        self.alpha_rate_control = gui.lineEdit(box, self, 'alpha_rate', 'Alpha rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alpha_rate'))
        self.lambda_shape_control = gui.lineEdit(box, self, 'lambda_shape', 'Lambda shape:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('lambda_shape'))
        self.lambda_rate_control = gui.lineEdit(box, self, 'lambda_rate', 'Lambda rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('lambda_rate'))
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
        node = SparseBayesianRegression()

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
    ow = OWSparseBayesianRegression()
    ow.show()
    app.exec_()