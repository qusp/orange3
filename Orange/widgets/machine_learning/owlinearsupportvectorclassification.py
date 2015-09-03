# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import LinearSupportVectorClassification


class OWLinearSupportVectorClassification(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Linear Support Vector Classification"
    description = "Use linear support vector machines to classify data instances. . See also scikit.sklearn.LinearSVC"
    author = "Christian Kothe"
    icon = "icons/LinearSupportVectorClassification.svg"
    priority = 8
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
    cost = Setting(None)
    loss = Setting(None)
    regularizer = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    max_iter = Setting(None)
    verbosity = Setting(None)
    class_weights = Setting(None)
    dual_formulation = Setting(None)
    include_bias = Setting(None)
    bias_scaling = Setting(None)
    random_seed = Setting(None)
    tolerance = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(LinearSupportVectorClassification())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('cost', self.node.cost)
            super().__setattr__('loss', self.node.loss)
            super().__setattr__('regularizer', self.node.regularizer)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('class_weights', self.node.class_weights)
            super().__setattr__('dual_formulation', self.node.dual_formulation)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('bias_scaling', self.node.bias_scaling)
            super().__setattr__('random_seed', self.node.random_seed)
            super().__setattr__('tolerance', self.node.tolerance)
        else:
            self.node.cost = self.cost
            self.node.loss = self.loss
            self.node.regularizer = self.regularizer
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.max_iter = self.max_iter
            self.node.verbosity = self.verbosity
            self.node.class_weights = self.class_weights
            self.node.dual_formulation = self.dual_formulation
            self.node.include_bias = self.include_bias
            self.node.bias_scaling = self.bias_scaling
            self.node.random_seed = self.random_seed
            self.node.tolerance = self.tolerance

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.cost_control = gui.lineEdit(box, self, 'cost', label='Cost:', orientation='horizontal', callback=lambda: self.property_changed('cost'), tooltip="SVM cost parameter. This is the parameter C of the error term.")
        self.loss_control = gui.comboBox(box, self, 'loss', label='Loss:', items=('l1', 'l2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('loss'), tooltip="Data loss function. l1 is the hinge loss (standard SVM), l2 is the squared hinge loss.")
        self.regularizer_control = gui.comboBox(box, self, 'regularizer', label='Regularizer:', items=('l1', 'l2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('regularizer'), tooltip="Regularization term. Selecting l2 (default) gives small weights, and l1 gives sparse weights.")
        self.search_metric_control = gui.comboBox(box, self, 'search_metric', label='Search metric:', items=('accuracy', 'average_prediction', 'f1', 'precision', 'recall', 'roc_auc', 'mean_absolute_error', 'mean_squared_error', 'r2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter (alpha) via cross-validation.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', label='Num folds:', orientation='horizontal', callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', label='Max iter:', orientation='horizontal', callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations. Additional stopping criterion to limit compute time.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', label='Verbosity:', orientation='horizontal', callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.class_weights_control = gui.lineEdit(box, self, 'class_weights', label='Class weights:', orientation='horizontal', callback=lambda: self.property_changed('class_weights'), tooltip="Per-class weights (dict). Optional.")
        self.dual_formulation_control = gui.checkBox(box, self, 'dual_formulation', label='Dual formulation', callback=lambda: self.property_changed('dual_formulation'), tooltip="Use dual formulation. If set, can be faster when #trials > #features, but doesn't support l1.")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', label='Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.bias_scaling_control = gui.lineEdit(box, self, 'bias_scaling', label='Bias scaling:', orientation='horizontal', callback=lambda: self.property_changed('bias_scaling'), tooltip="Scale for bias term. Since this implementation applies the regularization to the bias term too, you can use this scale to counter the effect.")
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', label='Random seed:', orientation='horizontal', callback=lambda: self.property_changed('random_seed'), tooltip="Random seed (int or None). Different values may give slightly different outcomes.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', label='Tolerance:', orientation='horizontal', callback=lambda: self.property_changed('tolerance'), tooltip="Convergence tolerance. Larger values give less accurate results but faster solution time.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
