# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import StochasticGradientDescentClassification


class OWStochasticGradientDescentClassification(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Stochastic Gradient Descent Classification"
    description = "Classification models learned via stochastic gradient descent."
    author = "Christian Kothe"
    icon = "icons/StochasticGradientDescentClassification.svg"
    priority = 16
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
        # Initialize with a newly instantiated node.
        super().__init__(StochasticGradientDescentClassification())

        # Set default properties.
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

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.loss_control = gui.lineEdit(box, self, 'loss', 'Loss:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('loss'), tooltip="Loss function to use. Hinge yields an SVM, log yields logistic regression, modified_huber is another smooth loss that enables probability outputs and tolerance to outliers, squared_hinge is like hinge but is quadratically penalized. Perceptron is the loss used by the perceptron algorithm. For the other losses, see StochasticGradientDescentRegression.")
        self.regularizer_control = gui.lineEdit(box, self, 'regularizer', 'Regularizer:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('regularizer'), tooltip="Regularization term. Selecting l2 (default) gives small weights, l1 gives sparse weights, and elasticnet is a combination of the two.")
        self.alphas_control = gui.lineEdit(box, self, 'alphas', 'Alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alphas'), tooltip="Regularization strength. Larger values cause stronger regularization.")
        self.l1_ratio_control = gui.lineEdit(box, self, 'l1_ratio', 'L1 ratio:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('l1_ratio'), tooltip="Ratio between l1 and l2 penalties. If set to 0, the penalty is l2, if set to 1, it is l1; anything in between is a mixture. When a list is given, the optimal parameter is selected; a good range is [0.1, 0.5, 0.7, 0.9, 0.95, 0.99, 1].")
        self.num_iter_control = gui.lineEdit(box, self, 'num_iter', 'Num iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_iter'), tooltip="Number of iterations. One iteration is one pass over the data.")
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'), tooltip="Number of parallel jobs. The value -1 means use all available CPU cores.")
        self.search_metric_control = gui.lineEdit(box, self, 'search_metric', 'Search metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter (alpha) via cross-validation.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', 'Probabilistic', callback=lambda: self.property_changed('probabilistic'), tooltip="Output probabilities instead of class labels.")
        self.warm_start_control = gui.checkBox(box, self, 'warm_start', 'Warm start', callback=lambda: self.property_changed('warm_start'), tooltip="Start from previous solution. This allows for online updating of the model.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.averaging_control = gui.lineEdit(box, self, 'averaging', 'Averaging:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('averaging'), tooltip="Use averaging. Can also be an int greater than 1; in this case, this is the number of samples seen after which averaging kicks in.")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.epsilon_control = gui.lineEdit(box, self, 'epsilon', 'Epsilon:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('epsilon'), tooltip="Epsilon for epsilon-insensitive and Huber losses. Note that this depends strongly on the scale of the data.")
        self.learning_rate_schedule_control = gui.lineEdit(box, self, 'learning_rate_schedule', 'Learning rate schedule:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('learning_rate_schedule'), tooltip="Schedule for adapting the learning rate. 'constant': eta=eta0, 'optimal': eta=1.0/(t+t0), 'invscaling': eta0/pow(t,power_t)")
        self.eta0_control = gui.lineEdit(box, self, 'eta0', 'Eta0:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('eta0'), tooltip="Initial learning rate.")
        self.power_t_control = gui.lineEdit(box, self, 'power_t', 'Power t:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('power_t'), tooltip="Exponent in invscaling schedule.")
        self.shuffle_control = gui.checkBox(box, self, 'shuffle', 'Shuffle', callback=lambda: self.property_changed('shuffle'), tooltip="Shuffle data after each epoch.")
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'), tooltip="Random seed (int or None). Different values may give slightly different outcomes.")
        self.class_weight_control = gui.lineEdit(box, self, 'class_weight', 'Class weight:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('class_weight'), tooltip="Per-class weights. If given as dict, allows to override the weights per class.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
