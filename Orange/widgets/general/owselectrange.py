# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import SelectRange


class OWSelectRange(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Prune Range"
    description = "Prune data based on a given range."
    author = "Christian Kothe"
    icon = "icons/SelectRange.svg"
    priority = 11
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
    selection = Setting(None)
    unit = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SelectRange())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('selection', self.node.selection)
            super().__setattr__('unit', self.node.unit)
        else:
            self.node.axis = self.axis
            self.node.selection = self.selection
            self.node.unit = self.unit

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.lineEdit(box, self, 'axis', 'Axis:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('axis'), tooltip="Axis to prune. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency', 'instance', 'feature', ...). ")
        self.selection_control = gui.lineEdit(box, self, 'selection', 'Selection:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('selection'), tooltip="Selection range. Can be a list of indices, a slice, or an expression string evaluating into indices.")
        self.unit_control = gui.lineEdit(box, self, 'unit', 'Unit:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('unit'), tooltip="Selection unit. Depending on the axis, different units are applicable.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
