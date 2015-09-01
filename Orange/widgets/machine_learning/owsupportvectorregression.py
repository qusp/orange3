# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.machine_learning import SupportVectorRegression


class OWSupportVectorRegression(widget.OWWidget):
    name = 'Support Vector Regression'
    description = 'Regression using support vector machines.'
    author = 'Christian Kothe'
    icon = 'icons/SupportVectorRegression.svg'
    priority = 19
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

    kernel = Setting(None)
    cost = Setting(None)
    poly_degree = Setting(None)
    gamma = Setting(None)
    coef0 = Setting(None)
    epsilon = Setting(None)
    tolerance = Setting(None)
    max_iter = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    verbosity = Setting(None)
    shrinking = Setting(None)
    cache_size = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = SupportVectorRegression()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('kernel', self.node.kernel)
            super().__setattr__('cost', self.node.cost)
            super().__setattr__('poly_degree', self.node.poly_degree)
            super().__setattr__('gamma', self.node.gamma)
            super().__setattr__('coef0', self.node.coef0)
            super().__setattr__('epsilon', self.node.epsilon)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('shrinking', self.node.shrinking)
            super().__setattr__('cache_size', self.node.cache_size)
        else:
            self.node.kernel = self.kernel
            self.node.cost = self.cost
            self.node.poly_degree = self.poly_degree
            self.node.gamma = self.gamma
            self.node.coef0 = self.coef0
            self.node.epsilon = self.epsilon
            self.node.tolerance = self.tolerance
            self.node.max_iter = self.max_iter
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.verbosity = self.verbosity
            self.node.shrinking = self.shrinking
            self.node.cache_size = self.cache_size

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.kernel_control = gui.lineEdit(box, self, 'kernel', 'Kernel:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('kernel'))
        self.cost_control = gui.lineEdit(box, self, 'cost', 'Cost:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('cost'))
        self.poly_degree_control = gui.lineEdit(box, self, 'poly_degree', 'Poly degree:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('poly_degree'))
        self.gamma_control = gui.lineEdit(box, self, 'gamma', 'Gamma:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('gamma'))
        self.coef0_control = gui.lineEdit(box, self, 'coef0', 'Coef0:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('coef0'))
        self.epsilon_control = gui.lineEdit(box, self, 'epsilon', 'Epsilon:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('epsilon'))
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'))
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.search_metric_control = gui.lineEdit(box, self, 'search_metric', 'Search metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('search_metric'))
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.shrinking_control = gui.checkBox(box, self, 'shrinking', 'Shrinking', callback=lambda: self.property_changed('shrinking'))
        self.cache_size_control = gui.lineEdit(box, self, 'cache_size', 'Cache size:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('cache_size'))
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
        node = SupportVectorRegression()

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
    ow = OWSupportVectorRegression()
    ow.show()
    app.exec_()