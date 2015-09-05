# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import PruneBadData


class OWPruneBadData(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Prune Bad Data"
    description = "Prune data based on a given value criterion. This node updates its removal mask on non-incremental chunks and carries the mask over to incremental chunks."
    author = "Christian Kothe"
    icon = "icons/PruneBadData.svg"
    priority = 8
    category = "General"

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
    axis = Setting(None)
    criteria = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(PruneBadData())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('criteria', self.node.criteria)
        else:
            self.node.axis = self.axis
            self.node.criteria = self.criteria

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('statistic', 'space', 'axis', 'instance', 'time', 'lag', 'feature', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis over which to prune. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency', 'instance', 'feature', ...).")
        self.criteria_control = gui.lineEdit(box, self, 'criteria', label='Criteria:', orientation='horizontal', callback=lambda: self.property_changed('criteria'), tooltip="Pruning criteria. Can be a set of multiple possible criteria.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
