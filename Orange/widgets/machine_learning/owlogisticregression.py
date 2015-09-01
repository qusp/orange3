# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.machine_learning import LogisticRegression


class OWLogisticRegression(widget.OWWidget):
    name = 'Logistic Regression'
    description = 'Use Logistic Regression (logreg) to classify data instances. . See also linear_model.LogisticRegression.'
    author = 'Christian Kothe'
    icon = 'icons/LogisticRegression.svg'
    priority = 9
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
        super().__init__()

        # Construct node instance and set default properties.
        self.node = LogisticRegression()
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

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.regularizer_control = gui.lineEdit(box, self, 'regularizer', 'Regularizer:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('regularizer'))
        self.alphas_control = gui.lineEdit(box, self, 'alphas', 'Alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alphas'))
        self.search_metric_control = gui.lineEdit(box, self, 'search_metric', 'Search metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('search_metric'))
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'))
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'))
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', 'Probabilistic', callback=lambda: self.property_changed('probabilistic'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.class_weights_control = gui.lineEdit(box, self, 'class_weights', 'Class weights:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('class_weights'))
        self.solver_control = gui.lineEdit(box, self, 'solver', 'Solver:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('solver'))
        self.dual_formulation_control = gui.checkBox(box, self, 'dual_formulation', 'Dual formulation', callback=lambda: self.property_changed('dual_formulation'))
        self.multiclass_control = gui.lineEdit(box, self, 'multiclass', 'Multiclass:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('multiclass'))
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'))
        self.bias_scaling_control = gui.lineEdit(box, self, 'bias_scaling', 'Bias scaling:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('bias_scaling'))
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'))
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
        node = LogisticRegression()

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
    ow = OWLogisticRegression()
    ow.show()
    app.exec_()