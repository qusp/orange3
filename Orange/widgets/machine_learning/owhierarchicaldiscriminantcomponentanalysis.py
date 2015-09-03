# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.machine_learning import HierarchicalDiscriminantComponentAnalysis


class OWHierarchicalDiscriminantComponentAnalysis(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Hierarchical Discriminant Component Analysis"
    description = "Use Hierarchical Discriminant Component Analysis (HDCA) to classify data instances."
    author = "Christian Kothe"
    icon = "icons/HierarchicalDiscriminantComponentAnalysis.svg"
    priority = 4
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
    shrinkage = Setting(None)
    probabilistic = Setting(None)
    class_weights = Setting(None)
    tolerance = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(HierarchicalDiscriminantComponentAnalysis())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('shrinkage', self.node.shrinkage)
            super().__setattr__('probabilistic', self.node.probabilistic)
            super().__setattr__('class_weights', self.node.class_weights)
            super().__setattr__('tolerance', self.node.tolerance)
        else:
            self.node.shrinkage = self.shrinkage
            self.node.probabilistic = self.probabilistic
            self.node.class_weights = self.class_weights
            self.node.tolerance = self.tolerance

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.shrinkage_control = gui.lineEdit(box, self, 'shrinkage', label='Shrinkage:', orientation='horizontal', callback=lambda: self.property_changed('shrinkage'), tooltip="Regularization strength. If using 'auto', the parameter is computed analytical (using the Ledoit-Wolf method); otherwise a number between 0 (least) and 1 (most) should be given.")
        self.probabilistic_control = gui.checkBox(box, self, 'probabilistic', label='Probabilistic', callback=lambda: self.property_changed('probabilistic'), tooltip="Output probabilities instead of class labels.")
        self.class_weights_control = gui.lineEdit(box, self, 'class_weights', label='Class weights:', orientation='horizontal', callback=lambda: self.property_changed('class_weights'), tooltip="Per-class weight (dictionary). Optional.")
        self.tolerance_control = gui.lineEdit(box, self, 'tolerance', label='Tolerance:', orientation='horizontal', callback=lambda: self.property_changed('tolerance'), tooltip="Threshold for rank estimation in SVD.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
