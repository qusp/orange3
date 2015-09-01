# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import RegularizedCommonSpatialPatterns


class OWRegularizedCommonSpatialPatterns(widget.OWWidget):
    name = "Regularized Common Spatial Patterns"
    description = "Filter the given signal using Regularized Common Spatial Patterns.Multiple regularizers are supported, and the default setting yieldsunregularized CSP."
    author = "Christian Kothe"
    icon = "icons/RegularizedCommonSpatialPatterns.svg"
    priority = 12
    category = "Filters"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': 0},
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

    want_main_area = False

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
        super().__init__()

        # Construct node instance and set default properties.
        self.node = RegularizedCommonSpatialPatterns()
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

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.mode_control = gui.lineEdit(box, self, 'mode', 'Mode:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('mode'))
        self.averaging_control = gui.lineEdit(box, self, 'averaging', 'Averaging:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('averaging'))
        self.nof_control = gui.lineEdit(box, self, 'nof', 'Nof:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('nof'))
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', 'Shrinkage:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('shrinkage'))
        self.tikhonov_control = gui.lineEdit(box, self, 'tikhonov', 'Tikhonov:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tikhonov'))
        self.smoothness_control = gui.lineEdit(box, self, 'smoothness', 'Smoothness:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('smoothness'))
        self.distance_scale_control = gui.lineEdit(box, self, 'distance_scale', 'Distance scale:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('distance_scale'))
        self.stationarity_control = gui.lineEdit(box, self, 'stationarity', 'Stationarity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('stationarity'))
        self.chunklen_control = gui.lineEdit(box, self, 'chunklen', 'Chunklen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('chunklen'))
        self.sparsity_control = gui.lineEdit(box, self, 'sparsity', 'Sparsity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('sparsity'))
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'))
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.invariance_control = gui.lineEdit(box, self, 'invariance', 'Invariance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('invariance'))
        self.normality_control = gui.lineEdit(box, self, 'normality', 'Normality:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('normality'))
        self.weighted_tikhonov_control = gui.checkBox(box, self, 'weighted_tikhonov', 'Weighted tikhonov', callback=lambda: self.property_changed('weighted_tikhonov'))
        self.prefer_lasso_control = gui.checkBox(box, self, 'prefer_lasso', 'Prefer lasso', callback=lambda: self.property_changed('prefer_lasso'))
        self.cv_metric_control = gui.lineEdit(box, self, 'cv_metric', 'Cv metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('cv_metric'))
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
        node = RegularizedCommonSpatialPatterns()

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

    def set_artifact_data(self, artifact_data):
        self.node.artifact_data = artifact_data

    def set_other_data(self, other_data):
        self.node.other_data = other_data


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWRegularizedCommonSpatialPatterns()
    ow.show()
    app.exec_()