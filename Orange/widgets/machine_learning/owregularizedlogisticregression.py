# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import RegularizedLogisticRegression


class OWRegularizedLogisticRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Regularized Logistic Regression"
    description = "Logistic regression with complex regularization terms (including trace norm and l1/l2 norm)."
    author = "Christian Kothe"
    icon = "icons/RegularizedLogisticRegression.svg"
    priority = 13
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
    penalty = Setting(None)
    group_axes = Setting(None)
    lambdas = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    num_jobs = Setting(None)
    probabilistic = Setting(None)
    verbosity = Setting(None)
    max_iter = Setting(None)
    inner_gtol = Setting(None)
    inner_max_iter = Setting(None)
    abs_tol = Setting(None)
    rel_tol = Setting(None)
    lfbgs_memory = Setting(None)
    init_rho = Setting(None)
    update_rho = Setting(None)
    rho_threshold = Setting(None)
    rho_incr = Setting(None)
    rho_decr = Setting(None)
    over_relaxation = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(RegularizedLogisticRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('penalty', self.node.penalty)
            super().__setattr__('group_axes', self.node.group_axes)
            super().__setattr__('lambdas', self.node.lambdas)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('probabilistic', self.node.probabilistic)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('inner_gtol', self.node.inner_gtol)
            super().__setattr__('inner_max_iter', self.node.inner_max_iter)
            super().__setattr__('abs_tol', self.node.abs_tol)
            super().__setattr__('rel_tol', self.node.rel_tol)
            super().__setattr__('lfbgs_memory', self.node.lfbgs_memory)
            super().__setattr__('init_rho', self.node.init_rho)
            super().__setattr__('update_rho', self.node.update_rho)
            super().__setattr__('rho_threshold', self.node.rho_threshold)
            super().__setattr__('rho_incr', self.node.rho_incr)
            super().__setattr__('rho_decr', self.node.rho_decr)
            super().__setattr__('over_relaxation', self.node.over_relaxation)
        else:
            self.node.penalty = self.penalty
            self.node.group_axes = self.group_axes
            self.node.lambdas = self.lambdas
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.num_jobs = self.num_jobs
            self.node.probabilistic = self.probabilistic
            self.node.verbosity = self.verbosity
            self.node.max_iter = self.max_iter
            self.node.inner_gtol = self.inner_gtol
            self.node.inner_max_iter = self.inner_max_iter
            self.node.abs_tol = self.abs_tol
            self.node.rel_tol = self.rel_tol
            self.node.lfbgs_memory = self.lfbgs_memory
            self.node.init_rho = self.init_rho
            self.node.update_rho = self.update_rho
            self.node.rho_threshold = self.rho_threshold
            self.node.rho_incr = self.rho_incr
            self.node.rho_decr = self.rho_decr
            self.node.over_relaxation = self.over_relaxation

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.penalty_control = gui.comboBox(box, self, 'penalty', label='Penalty:', items=['trace', 'l1/l2', 'l1', 'l2'], sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('penalty'), tooltip="Regularization term. The trace norm yields low-rank solutions, l1/l2 yields group-wise sparse solutions. The others are mostly included for completeness; it is more efficient to use LogisticRegression to apply these.")
        self.group_axes_control = gui.lineEdit(box, self, 'group_axes', label='Group axes:', orientation='horizontal', callback=lambda: self.property_changed('group_axes'), tooltip="Axes over which the penalty shall group. For the trace norm, 2 axes must be given.")
        self.lambdas_control = gui.lineEdit(box, self, 'lambdas', label='Lambdas:', orientation='horizontal', callback=lambda: self.property_changed('lambdas'), tooltip="Regularization strength. Larger values cause stronger regularization.")
        self.search_metric_control = gui.comboBox(box, self, 'search_metric', label='Search metric:', items=('accuracy', 'average_prediction', 'f1', 'precision', 'recall', 'roc_auc', 'mean_absolute_error', 'mean_squared_error', 'r2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter (alpha) via cross-validation.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', label='Num folds:', orientation='horizontal', callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', label='Num jobs:', orientation='horizontal', callback=lambda: self.property_changed('num_jobs'), tooltip="Number of parallel jobs. The value -1 means use all available CPU cores.")
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', label='Probabilistic', callback=lambda: self.property_changed('probabilistic'), tooltip="Output probabilities instead of class labels.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', label='Verbosity:', orientation='horizontal', callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', label='Max iter:', orientation='horizontal', callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of outer-loop iterations. Additional stopping criterion to limit compute time.")
        self.inner_gtol_control = gui.lineEdit(box, self, 'inner_gtol', label='Inner gtol:', orientation='horizontal', callback=lambda: self.property_changed('inner_gtol'), tooltip="LBFGS convergence tolerance. Larger values give less accurate results but faster solution time.")
        self.inner_max_iter_control = gui.lineEdit(box, self, 'inner_max_iter', label='Inner max iter:', orientation='horizontal', callback=lambda: self.property_changed('inner_max_iter'), tooltip="LBFGS maximum number of iterations for inner solver. Additional stopping criterion to limit compute time.")
        self.abs_tol_control = gui.lineEdit(box, self, 'abs_tol', label='Abs tol:', orientation='horizontal', callback=lambda: self.property_changed('abs_tol'), tooltip="ADMM absolute convergence tolerance.")
        self.rel_tol_control = gui.lineEdit(box, self, 'rel_tol', label='Rel tol:', orientation='horizontal', callback=lambda: self.property_changed('rel_tol'), tooltip="ADMM relative convergence tolerance.")
        self.lfbgs_memory_control = gui.lineEdit(box, self, 'lfbgs_memory', label='Lfbgs memory:', orientation='horizontal', callback=lambda: self.property_changed('lfbgs_memory'), tooltip="LBFGS memory length. This is the maximum number of variable-metric corrections tracked to approximate the inverse Hessian matrix.")
        self.init_rho_control = gui.lineEdit(box, self, 'init_rho', label='Init rho:', orientation='horizontal', callback=lambda: self.property_changed('init_rho'), tooltip="ADMM coupling parameter rho. Determines coupling strength between data term and regularization term.")
        self.update_rho_control = gui.checkBox(box, self, 'update_rho', label='Update rho', callback=lambda: self.property_changed('update_rho'), tooltip="Whether to update rho dynamically. Usually ensures better convergence, but can sometimes blow up.")
        self.rho_threshold_control = gui.lineEdit(box, self, 'rho_threshold', label='Rho threshold:', orientation='horizontal', callback=lambda: self.property_changed('rho_threshold'), tooltip="Rho update threshold.")
        self.rho_incr_control = gui.lineEdit(box, self, 'rho_incr', label='Rho incr:', orientation='horizontal', callback=lambda: self.property_changed('rho_incr'), tooltip="Rho update increment factor.")
        self.rho_decr_control = gui.lineEdit(box, self, 'rho_decr', label='Rho decr:', orientation='horizontal', callback=lambda: self.property_changed('rho_decr'), tooltip="Rho update decrement factor.")
        self.over_relaxation_control = gui.lineEdit(box, self, 'over_relaxation', label='Over relaxation:', orientation='horizontal', callback=lambda: self.property_changed('over_relaxation'), tooltip="ADMM over-relaxation parameter. 1.0 is no over-relaxation.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
