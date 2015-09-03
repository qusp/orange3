# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import RegularizedCommonSpatialPatterns


class OWRegularizedCommonSpatialPatterns(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Regularized Common Spatial Patterns"
    description = "Filter the given signal using Regularized Common Spatial Patterns.Multiple regularizers are supported, and the default setting yieldsunregularized CSP."
    author = "Christian Kothe"
    icon = "icons/RegularizedCommonSpatialPatterns.svg"
    priority = 12
    category = "Filters"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
        {'name': 'Artifact Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_artifact_data', 'flags': 0},
        {'name': 'Other Data', 'type': builtins.list, 'handler': 'set_other_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Artifact Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
        {'name': 'Other Data', 'type': builtins.list, 'flags': 0},
    ]

    # Configuration properties.
    mode = Setting(None)
    averaging = Setting(None)
    nof = Setting(None)
    shrinkage = Setting(None)
    tikhonov = Setting(None)
    smoothness = Setting(None)
    distance_scale = Setting(None)
    stationarity = Setting(None)
    chunklen = Setting(None)
    sparsity = Setting(None)
    num_folds = Setting(None)
    num_jobs = Setting(None)
    verbosity = Setting(None)
    invariance = Setting(None)
    normality = Setting(None)
    weighted_tikhonov = Setting(None)
    prefer_lasso = Setting(None)
    cv_metric = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(RegularizedCommonSpatialPatterns())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('mode', self.node.mode)
            super().__setattr__('averaging', self.node.averaging)
            super().__setattr__('nof', self.node.nof)
            super().__setattr__('shrinkage', self.node.shrinkage)
            super().__setattr__('tikhonov', self.node.tikhonov)
            super().__setattr__('smoothness', self.node.smoothness)
            super().__setattr__('distance_scale', self.node.distance_scale)
            super().__setattr__('stationarity', self.node.stationarity)
            super().__setattr__('chunklen', self.node.chunklen)
            super().__setattr__('sparsity', self.node.sparsity)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('invariance', self.node.invariance)
            super().__setattr__('normality', self.node.normality)
            super().__setattr__('weighted_tikhonov', self.node.weighted_tikhonov)
            super().__setattr__('prefer_lasso', self.node.prefer_lasso)
            super().__setattr__('cv_metric', self.node.cv_metric)
        else:
            self.node.mode = self.mode
            self.node.averaging = self.averaging
            self.node.nof = self.nof
            self.node.shrinkage = self.shrinkage
            self.node.tikhonov = self.tikhonov
            self.node.smoothness = self.smoothness
            self.node.distance_scale = self.distance_scale
            self.node.stationarity = self.stationarity
            self.node.chunklen = self.chunklen
            self.node.sparsity = self.sparsity
            self.node.num_folds = self.num_folds
            self.node.num_jobs = self.num_jobs
            self.node.verbosity = self.verbosity
            self.node.invariance = self.invariance
            self.node.normality = self.normality
            self.node.weighted_tikhonov = self.weighted_tikhonov
            self.node.prefer_lasso = self.prefer_lasso
            self.node.cv_metric = self.cv_metric

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.mode_control = gui.comboBox(box, self, 'mode', label='Mode:', items=['classification', 'regression'], sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('mode'), tooltip="Processing mode; classification is the typical CSP formulation, using 1-vs-rest for multiple classes. Regression is the SPoC formulation.")
        self.averaging_control = gui.comboBox(box, self, 'averaging', label='Averaging:', items=['mean', 'l1median'], sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('averaging'), tooltip="Covariance averaging across trials. The l1-median is robust.")
        self.nof_control = gui.lineEdit(box, self, 'nof', label='Nof:', orientation='horizontal', callback=lambda: self.property_changed('nof'), tooltip="Number of pattern pairs.")
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', label='Shrinkage:', orientation='horizontal', callback=lambda: self.property_changed('shrinkage'), tooltip="Shrinkage regularization. Higher values yield better-conditioned covariance matrices. A good range is [0, 0.1, 0.2,..., 0.9].")
        self.tikhonov_control = gui.lineEdit(box, self, 'tikhonov', label='Tikhonov:', orientation='horizontal', callback=lambda: self.property_changed('tikhonov'), tooltip="Tikhonov regularization. Higher values can yield better-behaved solutions. A good range is [0, 2^−8 , 2^−7, ...,2^−1].")
        self.smoothness_control = gui.lineEdit(box, self, 'smoothness', label='Smoothness:', orientation='horizontal', callback=lambda: self.property_changed('smoothness'), tooltip="Spatial smoothness regularization. Higher values yield smoother filters. A good range is [0, 2^−8 , 2^−7, ..., 2^−1].")
        self.distance_scale_control = gui.lineEdit(box, self, 'distance_scale', label='Distance scale:', orientation='horizontal', callback=lambda: self.property_changed('distance_scale'), tooltip="Distance scale for spatial smoothing. A good range is [0.01, 0.05, 0.1, 0.5, 0.8, 1.0, 1.2, 1.5].")
        self.stationarity_control = gui.lineEdit(box, self, 'stationarity', label='Stationarity:', orientation='horizontal', callback=lambda: self.property_changed('stationarity'), tooltip="Stationarity regularization. Higher values yield more stationary components. A good range is [0, 2^−8 , 2^−7, ..., 2^−1].")
        self.chunklen_control = gui.lineEdit(box, self, 'chunklen', label='Chunklen:', orientation='horizontal', callback=lambda: self.property_changed('chunklen'), tooltip="Stationary chunk length. This is the number of trials that shall be considered a chunk. Higher values yield larger-scale stationarity. A good range is [1, 5, 10].")
        self.sparsity_control = gui.lineEdit(box, self, 'sparsity', label='Sparsity:', orientation='horizontal', callback=lambda: self.property_changed('sparsity'), tooltip="Sparsity regularization. This is the number of non-zero channels. A good range is [1,2,3,4,5,7,9,11,16,32,64]")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', label='Num folds:', orientation='horizontal', callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', label='Num jobs:', orientation='horizontal', callback=lambda: self.property_changed('num_jobs'), tooltip="Number of jobs to run in parallel. -1 means auto-determine.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', label='Verbosity:', orientation='horizontal', callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.invariance_control = gui.lineEdit(box, self, 'invariance', label='Invariance:', orientation='horizontal', callback=lambda: self.property_changed('invariance'), tooltip="Invariance regularization. Higher values yield patterns that are more invariant under the given artifact signal (requires that the artifact_data parameter was assigned). A good range is [0, 2^−8, 2^−7, ..., 2^−1].")
        self.normality_control = gui.lineEdit(box, self, 'normality', label='Normality:', orientation='horizontal', callback=lambda: self.property_changed('normality'), tooltip="Normality regularization. Higher values shrink the solution towards data from other subjects. Requires that other_data is specified. A good range is [0, 0.1, 0.2,..., 0.9].")
        self.weighted_tikhonov_control = gui.checkBox(box, self, 'weighted_tikhonov', label='Weighted tikhonov', callback=lambda: self.property_changed('weighted_tikhonov'), tooltip="Use weighted Tikhonov regularization. Requires that other_data is specified.")
        self.prefer_lasso_control = gui.checkBox(box, self, 'prefer_lasso', label='Prefer lasso', callback=lambda: self.property_changed('prefer_lasso'), tooltip="Prefer lasso during parameter optimization. If set, lasso will also be used if the data has no additional axes; otherwise ridge regression will be used in this case.")
        self.cv_metric_control = gui.comboBox(box, self, 'cv_metric', label='Cv metric:', items=('accuracy', 'average_prediction', 'f1', 'precision', 'recall', 'roc_auc', 'mean_absolute_error', 'mean_squared_error', 'r2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('cv_metric'), tooltip="Cross-validation scoring metric.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data

    def set_artifact_data(self, artifact_data):
        self.node.artifact_data = artifact_data

    def set_other_data(self, other_data):
        self.node.other_data = other_data
