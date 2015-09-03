# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import PrincipalComponentAnalysis


class OWPrincipalComponentAnalysis(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Principal Component Analysis"
    description = "Reduce dimensionality using Principal Component Analysis (PCA)."
    author = "Christian Kothe"
    icon = "icons/PrincipalComponentAnalysis.svg"
    priority = 9
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
    num_components = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)
    whiten = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(PrincipalComponentAnalysis())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('num_components', self.node.num_components)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
            super().__setattr__('whiten', self.node.whiten)
        else:
            self.node.num_components = self.num_components
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes
            self.node.whiten = self.whiten

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.num_components_control = gui.lineEdit(box, self, 'num_components', label='Num components:', orientation='horizontal', callback=lambda: self.property_changed('num_components'), tooltip="Number of components to keep. If left unset, all components are kept.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any chunk will be processed.")
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', label='Domain axes:', orientation='horizontal', callback=lambda: self.property_changed('domain_axes'), tooltip="Axes which form the input domain of the transformation (e.g., a spatial decomposition like PCA on channels would have this set to 'space'. This is a  comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', label='Aggregate axes:', orientation='horizontal', callback=lambda: self.property_changed('aggregate_axes'), tooltip="Axes to aggregate statistics over. These are the axes that are treated as holding the statistical 'observations' or 'realizations'. For instance, a time-series model usually uses 'time' for this axis, and a method operating on trials/segments would use 'instance'. This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', label='Separate axes:', orientation='horizontal', callback=lambda: self.property_changed('separate_axes'), tooltip="Axes along which to learn separate models. This method can learn multiple separate and independent models (e.g., one per frequency, or one per time slice) in parallel. This is not a very common use case and thus argument is usually left empty (meaning: no axis). This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.whiten_control = gui.checkBox(box, self, 'whiten', label='Whiten', callback=lambda: self.property_changed('whiten'), tooltip="Normalize (whiten) outputs. This will decorrelate the features.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
