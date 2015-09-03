# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import LinearDiscriminantAnalysis


class OWLinearDiscriminantAnalysis(widget.OWWidget):
    name = "Linear Discriminant Analysis"
    description = "Use Linear Discriminant Analysis (LDA) to classify data instances. See also scikit.lda.LDA."
    author = "Christian Kothe"
    icon = "icons/LinearDiscriminantAnalysis.svg"
    priority = 7
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

    shrinkage = Setting(None)
    search_metric = Setting(None)
    num_folds = Setting(None)
    verbosity = Setting(None)
    probabilistic = Setting(None)
    solver = Setting(None)
    class_weights = Setting(None)
    tolerance = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = LinearDiscriminantAnalysis()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('shrinkage', self.node.shrinkage)
            super().__setattr__('search_metric', self.node.search_metric)
            super().__setattr__('num_folds', self.node.num_folds)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('probabilistic', self.node.probabilistic)
            super().__setattr__('solver', self.node.solver)
            super().__setattr__('class_weights', self.node.class_weights)
            super().__setattr__('tolerance', self.node.tolerance)
        else:
            self.node.shrinkage = self.shrinkage
            self.node.search_metric = self.search_metric
            self.node.num_folds = self.num_folds
            self.node.verbosity = self.verbosity
            self.node.probabilistic = self.probabilistic
            self.node.solver = self.solver
            self.node.class_weights = self.class_weights
            self.node.tolerance = self.tolerance

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', 'Shrinkage:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('shrinkage'), tooltip="Regularization strength. If using 'auto', the parameter is computed analytical (using the Ledoit-Wolf method); if using a list of numbers (between 0 and 1), a grid search is performed.")
        self.search_metric_control = gui.lineEdit(box, self, 'search_metric', 'Search metric:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('search_metric'), tooltip="Parameter search metric. This metric is used to optimize the regularization parameter if it is given as a list.")
        self.num_folds_control = gui.lineEdit(box, self, 'num_folds', 'Num folds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_folds'), tooltip="Number of cross-validation folds. Note that the data are not shuffled as they are assumed to stem from a time series.")
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'), tooltip="Verbosity level.")
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', 'Probabilistic', callback=lambda: self.property_changed('probabilistic'), tooltip="Output probabilities instead of class labels.")
        self.solver_control = gui.lineEdit(box, self, 'solver', 'Solver:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('solver'), tooltip="Solver to use. Supports the least-squares solution, eigenvalue decomposition, and singular-value decomposition based approaches; the svd method supports many features, but does not support shrinkage.")
        self.class_weights_control = gui.lineEdit(box, self, 'class_weights', 'Class weights:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('class_weights'), tooltip="Per-class weight (dictionary). Optional.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'), tooltip="Threshold for rank estimation in SVD.")
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
        node = LinearDiscriminantAnalysis()

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
    ow = OWLinearDiscriminantAnalysis()
    ow.show()
    app.exec_()