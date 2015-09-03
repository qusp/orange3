# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import StochasticGradientDescentRegression


class OWStochasticGradientDescentRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Stochastic Gradient Descent Regression"
    description = "Regularized regression models learned via stochastic gradient descent."
    author = "Christian Kothe"
    icon = "icons/StochasticGradientDescentRegression.svg"
    priority = 17
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
    loss = Setting(None)
    regularizer = Setting(None)
    alphas = Setting(None)
    l1_ratio = Setting(None)
    num_iter = Setting(None)
    warm_start = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    verbosity = Setting(None)
    averaging = Setting(None)
    include_bias = Setting(None)
    epsilon = Setting(None)
    learning_rate_schedule = Setting(None)
    eta0 = Setting(None)
    power_t = Setting(None)
    shuffle = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(StochasticGradientDescentRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('loss', self.node.loss)
            super().__setattr__('regularizer', self.node.regularizer)
            super().__setattr__('alphas', self.node.alphas)
            super().__setattr__('l1_ratio', self.node.l1_ratio)
            super().__setattr__('num_iter', self.node.num_iter)
            super().__setattr__('warm_start', self.node.warm_start)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('averaging', self.node.averaging)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('epsilon', self.node.epsilon)
            super().__setattr__('learning_rate_schedule', self.node.learning_rate_schedule)
            super().__setattr__('eta0', self.node.eta0)
            super().__setattr__('power_t', self.node.power_t)
            super().__setattr__('shuffle', self.node.shuffle)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.loss = self.loss
            self.node.regularizer = self.regularizer
            self.node.alphas = self.alphas
            self.node.l1_ratio = self.l1_ratio
            self.node.num_iter = self.num_iter
            self.node.warm_start = self.warm_start
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.verbosity = self.verbosity
            self.node.averaging = self.averaging
            self.node.include_bias = self.include_bias
            self.node.epsilon = self.epsilon
            self.node.learning_rate_schedule = self.learning_rate_schedule
            self.node.eta0 = self.eta0
            self.node.power_t = self.power_t
            self.node.shuffle = self.shuffle
            self.node.random_seed = self.random_seed

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.loss_control = gui.comboBox(box, self, 'loss', label='Loss:', items=('squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('loss'), tooltip="Loss function to use. Squared loss corresponds to traditional linear regression, huber fitting is a version robust to outliers, epsilon_insensitive is equivalent to support vector regression, and squared_epsilon_insensitive is a rarely used hybrid between linear and support vector regression.")
        self.regularizer_control = gui.comboBox(box, self, 'regularizer', label='Regularizer:', items=('l1', 'l2', 'elasticnet'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('regularizer'), tooltip="Regularization term. Selecting l2 (default) gives small weights, l1 gives sparse weights, and elasticnet is a combination of the two.")
        self.alphas_control = gui.lineEdit(box, self, 'alphas', label='Alphas:', orientation='horizontal', callback=lambda: self.property_changed('alphas'), tooltip="Regularization strength. Larger values cause stronger regularization.")
        self.l1_ratio_control = gui.lineEdit(box, self, 'l1_ratio', label='L1 ratio:', orientation='horizontal', callback=lambda: self.property_changed('l1_ratio'), tooltip="Ratio between l1 and l2 penalties. If set to 0, the penalty is l2, if set to 1, it is l1; anything in between is a mixture. When a list is given, the optimal parameter is selected; a good range is [0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1].")
        self.num_iter_control = gui.lineEdit(box, self, 'num_iter', label='Num iter:', orientation='horizontal', callback=lambda: self.property_changed('num_iter'), tooltip="Number of iterations. One iteration is one pass over the data.")
        self.warm_start_control = gui.checkBox(box, self, 'warm_start', label='Warm start', callback=lambda: self.property_changed('warm_start'), tooltip="Start from previous solution. This allows for online updating of the model.")
        self.search_metric_control = gui.comboBox(box, self, 'search_metric', label='Search metric:', items=('accuracy', 'average_prediction', 'f1', 'precision', 'recall', 'roc_auc', 'mean_absolute_error', 'mean_squared_error', 'r2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter (alpha) via cross-validation.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', label='Num folds:', orientation='horizontal', callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', label='Verbosity:', orientation='horizontal', callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.averaging_control = gui.lineEdit(box, self, 'averaging', label='Averaging:', orientation='horizontal', callback=lambda: self.property_changed('averaging'), tooltip="Use averaging. Can also be an int greater than 1; in this case, this is the number of samples seen after which averaging kicks in.")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', label='Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.epsilon_control = gui.lineEdit(box, self, 'epsilon', label='Epsilon:', orientation='horizontal', callback=lambda: self.property_changed('epsilon'), tooltip="Epsilon for epsilon-insensitive and Huber losses. Note that this depends strongly on the scale of the data.")
        self.learning_rate_schedule_control = gui.comboBox(box, self, 'learning_rate_schedule', label='Learning rate schedule:', items=('constant', 'optimal', 'invscaling'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('learning_rate_schedule'), tooltip="Schedule for adapting the learning rate. 'constant': eta=eta0, 'optimal': eta=1.0/(t+t0), 'invscaling': eta0/pow(t,power_t)")
        self.eta0_control = gui.lineEdit(box, self, 'eta0', label='Eta0:', orientation='horizontal', callback=lambda: self.property_changed('eta0'), tooltip="Initial learning rate.")
        self.power_t_control = gui.lineEdit(box, self, 'power_t', label='Power t:', orientation='horizontal', callback=lambda: self.property_changed('power_t'), tooltip="Exponent in invscaling schedule.")
        self.shuffle_control = gui.checkBox(box, self, 'shuffle', label='Shuffle', callback=lambda: self.property_changed('shuffle'), tooltip="Shuffle data after each epoch.")
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', label='Random seed:', orientation='horizontal', callback=lambda: self.property_changed('random_seed'), tooltip="Random seed (int or None). Different values may give slightly different outcomes.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
