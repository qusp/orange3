# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import ElasticNetRegression


class OWElasticNetRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Elastic Net Regression"
    description = "Implements the Elastic Net regression method (a form of sparse linear regression). See also sklearn.linear_model.ElasticNetCV."
    author = "Christian Kothe"
    icon = "icons/ElasticNetRegression.svg"
    priority = 3
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
    l1_ratio = Setting(None)
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
    positivity_constraint = Setting(None)
    precompute = Setting(None)
    selection = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ElasticNetRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('l1_ratio', self.node.l1_ratio)
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
            super().__setattr__('positivity_constraint', self.node.positivity_constraint)
            super().__setattr__('precompute', self.node.precompute)
            super().__setattr__('selection', self.node.selection)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.l1_ratio = self.l1_ratio
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
            self.node.positivity_constraint = self.positivity_constraint
            self.node.precompute = self.precompute
            self.node.selection = self.selection
            self.node.random_seed = self.random_seed

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.l1_ratio_control = gui.lineEdit(box, self, 'l1_ratio', 'L1 ratio:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('l1_ratio'), tooltip="Ratio between l1 and l2 penalties. If set to 0, the penalty is l2, if set to 1, it is l1; anything in between is a mixture. When a list is given, the optimal parameter is selected.")
        self.num_alphas_control = gui.lineEdit(box, self, 'num_alphas', 'Num alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_alphas'), tooltip="Number of alpha values to fit. This determines how densely the regularization path is explored.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations. Additional stopping criterion to limit compute time.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'), tooltip="Optimization tolerance. The default stopping criterion. Can be increased to speed up computation.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'), tooltip="Number of parallel jobs. The value -1 means use all available CPU cores.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', 'Normalize features', callback=lambda: self.property_changed('normalize_features'), tooltip="Normalize features. Should only be disabled if the data comes in with a predictable scale (e.g., normalized in some other way).")
        self.min_alpha_control = gui.lineEdit(box, self, 'min_alpha', 'Min alpha:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('min_alpha'), tooltip="Minimum regularization strength. This is expressed as a factor of the maximum regularization strength, which is calculated from the data.")
        self.alphas_control = gui.lineEdit(box, self, 'alphas', 'Alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alphas'), tooltip="Override regularization strengths. Optionally the alpha values to search over can be given here (instead of the auto-generated list based on num_alphas and epsilon).")
        self.positivity_constraint_control = gui.checkBox(box, self, 'positivity_constraint', 'Positivity constraint', callback=lambda: self.property_changed('positivity_constraint'), tooltip="Constrain weights to be positive.")
        self.precompute_control = gui.lineEdit(box, self, 'precompute', 'Precompute:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('precompute'), tooltip="Precompute shared data. Precompute some shared data that is reused during parameter search. Aside from 'auto', can be True, False, or the actual Gram matrix.")
        self.selection_control = gui.lineEdit(box, self, 'selection', 'Selection:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('selection'), tooltip="Parameter update schedule. Random can be significantly faster for higher tol settings.")
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'), tooltip="Random seed (int or None). Different values may give slightly different outcomes.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
