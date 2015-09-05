# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.general import FoldIntoAxis


class OWFoldIntoAxis(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Fold Into Axis"
    description = "Fold an axis into another axis. The target axis must have per-element names (e.g., space, feature). This will generate an elongated axis that has new names of the form OldName-1, OldName-2, OldName-3, etc."
    author = "Christian Kothe"
    icon = "icons/FoldIntoAxis.svg"
    priority = 6
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
    src_axis = Setting(None)
    dst_axis = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(FoldIntoAxis())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('src_axis', self.node.src_axis)
            super().__setattr__('dst_axis', self.node.dst_axis)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.src_axis = self.src_axis
            self.node.dst_axis = self.dst_axis
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.src_axis_control = gui.comboBox(box, self, 'src_axis', label='Src axis:', items=('statistic', 'space', 'axis', 'instance', 'time', 'lag', 'feature', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('src_axis'), tooltip="Axis to fold. This is the type of the axis that shall be folded into another axis.")
        self.dst_axis_control = gui.comboBox(box, self, 'dst_axis', label='Dst axis:', items=('statistic', 'space', 'axis', 'instance', 'time', 'lag', 'feature', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('dst_axis'), tooltip="Axis to fold into. This is the axis into which the other one shall be folded.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any numeric chunk data will be processed.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
