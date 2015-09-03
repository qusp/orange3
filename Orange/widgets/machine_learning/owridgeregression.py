# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import RidgeRegression


class OWRidgeRegression(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Ridge Regression"
    description = "Implements the ridge regression method (a regularized form of linear regression). See also sklearn.linear_model.RidgeCV."
    author = "Christian Kothe"
    icon = "icons/RidgeRegression.svg"
    priority = 14
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
    alphas = Setting(None)
    search_metric = Setting(None)
    normalize_features = Setting(None)
    include_bias = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(RidgeRegression())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('alphas', self.node.alphas)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('normalize_features', self.node.normalize_features)
            super().__setattr__('include_bias', self.node.include_bias)
        else:
            self.node.alphas = self.alphas
            self.node.search_metric = self.search_metric
            self.node.normalize_features = self.normalize_features
            self.node.include_bias = self.include_bias

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.alphas_control = gui.lineEdit(box, self, 'alphas', label='Alphas:', orientation='horizontal', callback=lambda: self.property_changed('alphas'), tooltip="Regularization strength. Larger values cause stronger regularization. The default is  intentionally coarse for quick turnaround -- refine it for  better results.")
        self.search_metric_control = gui.comboBox(box, self, 'search_metric', label='Search metric:', items=('accuracy', 'average_prediction', 'f1', 'precision', 'recall', 'roc_auc', 'mean_absolute_error', 'mean_squared_error', 'r2'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter (alpha) via cross-validation.")
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', label='Normalize features', callback=lambda: self.property_changed('normalize_features'), tooltip="Normalize features. Should only be disabled if the data comes in with a predictable scale (e.g., normalized in some other way).")
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', label='Include bias', callback=lambda: self.property_changed('include_bias'), tooltip="Include bias term. If false, your data needs to be centered or include a dummy feature set to 1.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
