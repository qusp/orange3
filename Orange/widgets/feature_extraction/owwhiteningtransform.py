# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.feature_extraction import WhiteningTransform


class OWWhiteningTransform(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Whitening Transform"
    description = "Whiten (decorrelate and normalize) the given data without rotation."
    author = "Christian Kothe"
    icon = "icons/WhiteningTransform.svg"
    priority = 12
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
    shrinkage = Setting(None)
    center = Setting(None)
    decorrelate = Setting(None)
    retain_axes = Setting(None)
    only_signals = Setting(None)
    domain_axes = Setting(None)
    aggregate_axes = Setting(None)
    separate_axes = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(WhiteningTransform())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('shrinkage', self.node.shrinkage)
            super().__setattr__('center', self.node.center)
            super().__setattr__('decorrelate', self.node.decorrelate)
            super().__setattr__('retain_axes', self.node.retain_axes)
            super().__setattr__('only_signals', self.node.only_signals)
            super().__setattr__('domain_axes', self.node.domain_axes)
            super().__setattr__('aggregate_axes', self.node.aggregate_axes)
            super().__setattr__('separate_axes', self.node.separate_axes)
        else:
            self.node.shrinkage = self.shrinkage
            self.node.center = self.center
            self.node.decorrelate = self.decorrelate
            self.node.retain_axes = self.retain_axes
            self.node.only_signals = self.only_signals
            self.node.domain_axes = self.domain_axes
            self.node.aggregate_axes = self.aggregate_axes
            self.node.separate_axes = self.separate_axes

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', label='Shrinkage:', orientation='horizontal', callback=lambda: self.property_changed('shrinkage'), tooltip="Regularization strength. This is primarily to prevent degenerate solutions.")
        self.center_control = gui.checkBox(box, self, 'center', label='Center', callback=lambda: self.property_changed('center'), tooltip="Center data before whitening. This will remove the mean.")
        self.decorrelate_control = gui.checkBox(box, self, 'decorrelate', label='Decorrelate', callback=lambda: self.property_changed('decorrelate'), tooltip="Decorrelate the data. If False, only normalization will be performed.")
        self.retain_axes_control = gui.checkBox(box, self, 'retain_axes', label='Retain axes', callback=lambda: self.property_changed('retain_axes'), tooltip="Retain original axes. If false, the domain axes will be replaced by a FeatureAxis.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any chunk will be processed.")
        self.domain_axes_control = gui.lineEdit(box, self, 'domain_axes', label='Domain axes:', orientation='horizontal', callback=lambda: self.property_changed('domain_axes'), tooltip="Axes which form the input domain of the transformation (e.g., a spatial decomposition like PCA on channels would have this set to 'space'. This is a  comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.aggregate_axes_control = gui.lineEdit(box, self, 'aggregate_axes', label='Aggregate axes:', orientation='horizontal', callback=lambda: self.property_changed('aggregate_axes'), tooltip="Axes to aggregate statistics over. These are the axes that are treated as holding the statistical 'observations' or 'realizations'. For instance, a time-series model usually uses 'time' for this axis, and a method operating on trials/segments would use 'instance'. This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.separate_axes_control = gui.lineEdit(box, self, 'separate_axes', label='Separate axes:', orientation='horizontal', callback=lambda: self.property_changed('separate_axes'), tooltip="Axes along which to learn separate models. This method can learn multiple separate and independent models (e.g., one per frequency, or one per time slice) in parallel. This is not a very common use case and thus argument is usually left empty (meaning: no axis). This is a comma-separated list of axis names, possibly empty, or the special string '(all others)'.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
