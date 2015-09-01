# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import OnlineDictionaryLearning


class OWOnlineDictionaryLearning(widget.OWWidget):
    name = 'Online Dictionary Learning'
    description = 'Perform online sparse dictionary learning.'
    author = 'Christian Kothe'
    icon = 'icons/OnlineDictionaryLearning.svg'
    priority = 7
    category = 'Feature_Extraction'

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

    num_components = Setting(None)
    alpha = Setting(None)
    transform_alpha = Setting(None)
    batch_size = Setting(None)
    max_iter = Setting(None)
    num_jobs = Setting(None)
    verbosity = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)
    shuffle = Setting(None)
    transform_nonzeroes = Setting(None)
    fit_algorithm = Setting(None)
    transform_algorithm = Setting(None)
    split_sign = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = OnlineDictionaryLearning()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_components', self.node.num_components)
            super().__setattr__('alpha', self.node.alpha)
            super().__setattr__('transform_alpha', self.node.transform_alpha)
            super().__setattr__('batch_size', self.node.batch_size)
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('num_jobs', self.node.num_jobs)
            super().__setattr__('verbosity', self.node.verbosity)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
            super().__setattr__('shuffle', self.node.shuffle)
            super().__setattr__('transform_nonzeroes', self.node.transform_nonzeroes)
            super().__setattr__('fit_algorithm', self.node.fit_algorithm)
            super().__setattr__('transform_algorithm', self.node.transform_algorithm)
            super().__setattr__('split_sign', self.node.split_sign)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.num_components = self.num_components
            self.node.alpha = self.alpha
            self.node.transform_alpha = self.transform_alpha
            self.node.batch_size = self.batch_size
            self.node.max_iter = self.max_iter
            self.node.num_jobs = self.num_jobs
            self.node.verbosity = self.verbosity
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes
            self.node.shuffle = self.shuffle
            self.node.transform_nonzeroes = self.transform_nonzeroes
            self.node.fit_algorithm = self.fit_algorithm
            self.node.transform_algorithm = self.transform_algorithm
            self.node.split_sign = self.split_sign
            self.node.random_seed = self.random_seed

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_components_control = gui.lineEdit(box, self, 'num_components', 'Num components:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_components'))
        self.alpha_control = gui.lineEdit(box, self, 'alpha', 'Alpha:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('alpha'))
        self.transform_alpha_control = gui.lineEdit(box, self, 'transform_alpha', 'Transform alpha:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('transform_alpha'))
        self.batch_size_control = gui.lineEdit(box, self, 'batch_size', 'Batch size:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('batch_size'))
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'))
        self.num_jobs_control = gui.lineEdit(box, self, 'num_jobs', 'Num jobs:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_jobs'))
        self.verbosity_control = gui.lineEdit(box, self, 'verbosity', 'Verbosity:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('verbosity'))
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'))
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', 'Domain axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('domain_axes'))
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', 'Aggregate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('aggregate_axes'))
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', 'Separate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('separate_axes'))
        self.shuffle_control = gui.checkBox(box, self, 'shuffle', 'Shuffle', callback=lambda: self.property_changed('shuffle'))
        self.transform_nonzeroes_control = gui.lineEdit(box, self, 'transform_nonzeroes', 'Transform nonzeroes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('transform_nonzeroes'))
        self.fit_algorithm_control = gui.lineEdit(box, self, 'fit_algorithm', 'Fit algorithm:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('fit_algorithm'))
        self.transform_algorithm_control = gui.lineEdit(box, self, 'transform_algorithm', 'Transform algorithm:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('transform_algorithm'))
        self.split_sign_control = gui.checkBox(box, self, 'split_sign', 'Split sign', callback=lambda: self.property_changed('split_sign'))
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'))
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
        node = OnlineDictionaryLearning()

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
    ow = OWOnlineDictionaryLearning()
    ow.show()
    app.exec_()