# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import FastICA


class OWFastICA(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Independent Component Analysis (FastICA)"
    description = "Perform independent component analysis using the FastICA method."
    author = "Christian Kothe"
    icon = "icons/FastICA.svg"
    priority = 3
    category = "Feature_Extraction"

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
    max_iter = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)
    num_components = Setting(None)
    algorithm = Setting(None)
    whiten = Setting(None)
    fun = Setting(None)
    tolerance = Setting(None)
    random_seed = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(FastICA())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('max_iter', self.node.max_iter)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
            super().__setattr__('num_components', self.node.num_components)
            super().__setattr__('algorithm', self.node.algorithm)
            super().__setattr__('whiten', self.node.whiten)
            super().__setattr__('fun', self.node.fun)
            super().__setattr__('tolerance', self.node.tolerance)
            super().__setattr__('random_seed', self.node.random_seed)
        else:
            self.node.max_iter = self.max_iter
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes
            self.node.num_components = self.num_components
            self.node.algorithm = self.algorithm
            self.node.whiten = self.whiten
            self.node.fun = self.fun
            self.node.tolerance = self.tolerance
            self.node.random_seed = self.random_seed

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.max_iter_control = gui.lineEdit(box, self, 'max_iter', 'Max iter:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_iter'), tooltip="Maximum number of iterations.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', 'Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any chunk will be processed.")
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', 'Domain axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('domain_axes'), tooltip="Axes which form the input domain of the transformation (e.g., a spatial decomposition like PCA on channels would have this set to 'space'. This is a  comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', 'Aggregate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('aggregate_axes'), tooltip="Axes to aggregate statistics over. These are the axes that are treated as holding the statistical 'observations' or 'realizations'. For instance, a time-series model usually uses 'time' for this axis, and a method operating on trials/segments would use 'instance'. This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', 'Separate axes:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('separate_axes'), tooltip="Axes along which to learn separate models. This method can learn multiple separate and independent models (e.g., one per frequency, or one per time slice) in parallel. This is not a very common use case and thus argument is usually left empty (meaning: no axis). This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.num_components_control = gui.lineEdit(box, self, 'num_components', 'Num components:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_components'), tooltip="Number of components to keep. If left unset, all components are kept.")
        self.algorithm_control = gui.lineEdit(box, self, 'algorithm', 'Algorithm:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('algorithm'), tooltip="Optimization approach. For highly noisy data the parallel approach is usually better.")
        self.whiten_control = gui.checkBox(box, self, 'whiten', 'Whiten', callback=lambda: self.property_changed('whiten'), tooltip="Pre-whiten the data. If disabled, the data must have been whitened otherwise before.")
        self.fun_control = gui.lineEdit(box, self, 'fun', 'Fun:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('fun'), tooltip="Non-linearity to use. The logcosh function corresponds to Infomax ICA.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', 'Tolerance:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tolerance'), tooltip="Tolerance for optimization. Serves as a stopping criterion.")
        self.random_seed_control = gui.lineEdit(box, self, 'random_seed', 'Random seed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('random_seed'), tooltip="Random seed (int or None). Different values may give slightly different outcomes.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
