# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import LarsRegression


class OWLarsRegression(widget.OWWidget):
    name = "LARS Regression"
    description = "Implements the LARS regression method (a form of sparse linear regression). See also sklearn.linear_model.LarsCV."
    author = "Christian Kothe"
    icon = "icons/LarsRegression.svg"
    priority = 6
    category = "Machine_Learning"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    num_folds = Setting(None)
    num_alphas = Setting(None)
    max_iter = Setting(None)
    num_jobs = Setting(None)
    verbosity = Setting(None)
    normalize_features = Setting(None)
    include_bias = Setting(None)
    precompute = Setting(None)
    epsilon = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = LarsRegression()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('num_alphas', self.node.num_alphas)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('normalize_features', self.node.normalize_features)
            super().__setattr__('include_bias', self.node.include_bias)
            super().__setattr__('precompute', self.node.precompute)
            super().__setattr__('epsilon', self.node.epsilon)
        else:
            self.node.num_folds = self.num_folds
            self.node.num_alphas = self.num_alphas
            self.node.max_iter = self.max_iter
            self.node.num_jobs = self.num_jobs
            self.node.verbosity = self.verbosity
            self.node.normalize_features = self.normalize_features
            self.node.include_bias = self.include_bias
            self.node.precompute = self.precompute
            self.node.epsilon = self.epsilon

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'))
        self.num_alphas_control = gui.lineEdit(box, self, 'num_alphas', 'Num alphas:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_alphas'))
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.normalize_features_control = gui.checkBox(box, self, 'normalize_features', 'Normalize features', callback=lambda: self.property_changed('normalize_features'))
        self.include_bias_control = gui.checkBox(box, self, 'include_bias', 'Include bias', callback=lambda: self.property_changed('include_bias'))
        self.precompute_control = gui.lineEdit(box, self, 'precompute', 'Precompute:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('precompute'))
        self.epsilon_control = gui.lineEdit(box, self, 'epsilon', 'Epsilon:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('epsilon'))
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
        node = LarsRegression()

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
    ow = OWLarsRegression()
    ow.show()
    app.exec_()