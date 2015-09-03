# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import LogisticRegression


class OWLogisticRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Logistic Regression"
    description = "Use Logistic Regression (logreg) to classify data instances. . See also linear_model.LogisticRegression."
    author = "Christian Kothe"
    icon = "icons/LogisticRegression.svg"
    priority = 9
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
    regularizer = Setting(None)
    alphas = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    num_jobs = Setting(None)
    probabilistic = Setting(None)
    verbosity = Setting(None)
    class_weights = Setting(None)
    solver = Setting(None)
    dual_formulation = Setting(None)
    multiclass = Setting(None)
    max_iter = Setting(None)
    include_bias = Setting(None)
    bias_scaling = Setting(None)
    tolerance = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(LogisticRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('regularizer', self.node.regularizer)
            super().__setattr__('alphas', self.node.alphas)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('probabilistic', self.node.probabilistic)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('class_weights', self.node.class_weights)
            super().__setattr__('solver', self.node.solver)
            super().__setattr__('dual_formulation', self.node.dual_formulation)
            super().__setattr__('multiclass', self.node.multiclass)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('bias_scaling', self.node.bias_scaling)
            super().__setattr__('tolerance', self.node.tolerance)
        else:
            self.node.regularizer = self.regularizer
            self.node.alphas = self.alphas
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.num_jobs = self.num_jobs
            self.node.probabilistic = self.probabilistic
            self.node.verbosity = self.verbosity
            self.node.class_weights = self.class_weights
            self.node.solver = self.solver
            self.node.dual_formulation = self.dual_formulation
            self.node.multiclass = self.multiclass
            self.node.max_iter = self.max_iter
            self.node.include_bias = self.include_bias
            self.node.bias_scaling = self.bias_scaling
            self.node.tolerance = self.tolerance

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.regularizer_control = gui.lineEdit(box, self, 'regularizer', 'Regularizer:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('regularizer'), tooltip="Regularization term. Selecting l2 (default) gives small weights, and l1 gives sparse weights. If l1 is selected, the liblinear solver is automatically used.")
        self.alphas_control = gui.lineEdit(box, self, 'alphas', 'Alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alphas'), tooltip="Regularization strength. Larger values cause stronger regularization (Note for scikit-learn users: this is the inverse of C in logreg).")
        self.search_metric_control = gui.lineEdit(box, self, 'search_metric', 'Search metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter (alpha) via cross-validation.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'), tooltip="Number of parallel jobs. The value -1 means use all available CPU cores.")
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', 'Probabilistic', callback=lambda: self.property_changed('probabilistic'), tooltip="Output probabilities instead of class labels.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.class_weights_control = gui.lineEdit(box, self, 'class_weights', 'Class weights:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('class_weights'), tooltip="Per-class weights (dict). Optional.")
        self.solver_control = gui.lineEdit(box, self, 'solver', 'Solver:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('solver'), tooltip="Algorithm to use. L1 is only supported with liblinear.")
        self.dual_formulation_control = gui.checkBox(box, self, 'dual_formulation', 'Dual formulation', callback=lambda: self.property_changed('dual_formulation'), tooltip="Use dual formulation. If set, can be faster when #trials > #features, but doesn't support l1.")
        self.multiclass_control = gui.lineEdit(box, self, 'multiclass', 'Multiclass:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('multiclass'), tooltip="Multi-class formulation. Multinomial is only support for lbfgs.")
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations. Additional stopping criterion to limit compute time.")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.bias_scaling_control = gui.lineEdit(box, self, 'bias_scaling', 'Bias scaling:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('bias_scaling'), tooltip="Scale for bias term. Since this logreg implementation applies the regularization to the bias term too, you can use this scale to counter the effect.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'), tooltip="Convergence tolerance. Larger values give less accurate results but faster solution time.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
