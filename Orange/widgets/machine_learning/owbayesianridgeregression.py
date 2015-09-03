# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import BayesianRidgeRegression


class OWBayesianRidgeRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Bayesian Ridge Regression"
    description = "Implements the Bayesian ridge regression method (a regularized form of linear regression). See also sklearn.linear_model.BayesianRidge."
    author = "Christian Kothe"
    icon = "icons/BayesianRidgeRegression.svg"
    priority = 1
    category = "Machine_Learning"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    max_iter = Setting(None)
    tolerance = Setting(None)
    verbosity = Setting(None)
    include_bias = Setting(None)
    normalize_features = Setting(None)
    alpha_shape = Setting(None)
    alpha_rate = Setting(None)
    lambda_shape = Setting(None)
    lambda_rate = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(BayesianRidgeRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('normalize_features', self.node.normalize_features)
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
            self.node.alpha_shape = self.alpha_shape
            self.node.alpha_rate = self.alpha_rate
            self.node.lambda_shape = self.lambda_shape
            self.node.lambda_rate = self.lambda_rate

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations. Additional stopping criterion to limit compute time.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'), tooltip="Optimization tolerance. The default stopping criterion. Can be increased to speed up computation.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', 'Normalize features', callback=lambda: self.property_changed('normalize_features'), tooltip="Normalize features. Should only be disabled if the data comes in with a predictable scale (e.g., normalized in some other way).")
        self.alpha_shape_control = gui.lineEdit(box, self, 'alpha_shape', 'Alpha shape:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alpha_shape'), tooltip="Alpha shape parameter. Shape parameter for the Gamma distribution prior over the alpha parameter.")
        self.alpha_rate_control = gui.lineEdit(box, self, 'alpha_rate', 'Alpha rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alpha_rate'), tooltip="Alpha rate parameter. Rate parameter for the Gamma distribution prior over the alpha parameter.")
        self.lambda_shape_control = gui.lineEdit(box, self, 'lambda_shape', 'Lambda shape:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('lambda_shape'), tooltip="Lambda shape parameter. Shape parameter for the Gamma distribution prior over the lambda parameter.")
        self.lambda_rate_control = gui.lineEdit(box, self, 'lambda_rate', 'Lambda rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('lambda_rate'), tooltip="Lambda rate parameter. Rate parameter for the Gamma distribution prior over the lambda parameter.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
