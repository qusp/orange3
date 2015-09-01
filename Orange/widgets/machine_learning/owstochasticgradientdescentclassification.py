# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.machine_learning import StochasticGradientDescentClassification


class OWStochasticGradientDescentClassification(widget.OWWidget):
    name = 'Stochastic Gradient Descent Classification'
    description = 'Classification models learned via stochastic gradient descent.'
    author = 'Christian Kothe'
    icon = 'icons/StochasticGradientDescentClassification.svg'
    priority = 16
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

    loss = Setting(None)
    regularizer = Setting(None)
    alphas = Setting(None)
    l1_ratio = Setting(None)
    num_iter = Setting(None)
    num_jobs = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    probabilistic = Setting(None)
    warm_start = Setting(None)
    verbosity = Setting(None)
    averaging = Setting(None)
    include_bias = Setting(None)
    epsilon = Setting(None)
    learning_rate_schedule = Setting(None)
    eta0 = Setting(None)
    power_t = Setting(None)
    shuffle = Setting(None)
    random_seed = Setting(None)
    class_weight = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = StochasticGradientDescentClassification()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('loss', self.node.loss)
            super().__setattr__('regularizer', self.node.regularizer)
            super().__setattr__('alphas', self.node.alphas)
            super().__setattr__('l1_ratio', self.node.l1_ratio)
            super().__setattr__('num_iter', self.node.num_iter)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('probabilistic', self.node.probabilistic)
            super().__setattr__('warm_start', self.node.warm_start)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('averaging', self.node.averaging)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('epsilon', self.node.epsilon)
            super().__setattr__('learning_rate_schedule', self.node.learning_rate_schedule)
            super().__setattr__('eta0', self.node.eta0)
            super().__setattr__('power_t', self.node.power_t)
            super().__setattr__('shuffle', self.node.shuffle)
            super().__setattr__('random_seed', self.node.random_seed)
            super().__setattr__('class_weight', self.node.class_weight)
        else:
            self.node.loss = self.loss
            self.node.regularizer = self.regularizer
            self.node.alphas = self.alphas
            self.node.l1_ratio = self.l1_ratio
            self.node.num_iter = self.num_iter
            self.node.num_jobs = self.num_jobs
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.probabilistic = self.probabilistic
            self.node.warm_start = self.warm_start
            self.node.verbosity = self.verbosity
            self.node.averaging = self.averaging
            self.node.include_bias = self.include_bias
            self.node.epsilon = self.epsilon
            self.node.learning_rate_schedule = self.learning_rate_schedule
            self.node.eta0 = self.eta0
            self.node.power_t = self.power_t
            self.node.shuffle = self.shuffle
            self.node.random_seed = self.random_seed
            self.node.class_weight = self.class_weight

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.loss_control = gui.lineEdit(box, self, 'loss', 'Loss:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('loss'))
        self.regularizer_control = gui.lineEdit(box, self, 'regularizer', 'Regularizer:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('regularizer'))
        self.alphas_control = gui.lineEdit(box, self, 'alphas', 'Alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alphas'))
        self.l1_ratio_control = gui.lineEdit(box, self, 'l1_ratio', 'L1 ratio:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('l1_ratio'))
        self.num_iter_control = gui.lineEdit(box, self, 'num_iter', 'Num iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_iter'))
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'))
        self.search_metric_control = gui.lineEdit(box, self, 'search_metric', 'Search metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('search_metric'))
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'))
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', 'Probabilistic', callback=lambda: self.property_changed('probabilistic'))
        self.warm_start_control = gui.checkBox(box, self, 'warm_start', 'Warm start', callback=lambda: self.property_changed('warm_start'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.averaging_control = gui.lineEdit(box, self, 'averaging', 'Averaging:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('averaging'))
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'))
        self.epsilon_control = gui.lineEdit(box, self, 'epsilon', 'Epsilon:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('epsilon'))
        self.learning_rate_schedule_control = gui.lineEdit(box, self, 'learning_rate_schedule', 'Learning rate schedule:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('learning_rate_schedule'))
        self.eta0_control = gui.lineEdit(box, self, 'eta0', 'Eta0:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('eta0'))
        self.power_t_control = gui.lineEdit(box, self, 'power_t', 'Power t:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('power_t'))
        self.shuffle_control = gui.checkBox(box, self, 'shuffle', 'Shuffle', callback=lambda: self.property_changed('shuffle'))
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'))
        self.class_weight_control = gui.lineEdit(box, self, 'class_weight', 'Class weight:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('class_weight'))
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
        node = StochasticGradientDescentClassification()

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
    ow = OWStochasticGradientDescentClassification()
    ow.show()
    app.exec_()