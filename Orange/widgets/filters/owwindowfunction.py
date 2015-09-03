# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import WindowFunction


class OWWindowFunction(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Window Function"
    description = "Apply a window function to the given data across some specified axis."
    author = "Christian Kothe"
    icon = "icons/WindowFunction.svg"
    priority = 15
    category = "Filters"

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
    func = Setting(None)
    param = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(WindowFunction())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('func', self.node.func)
            super().__setattr__('param', self.node.param)
        else:
            self.node.axis = self.axis
            self.node.func = self.func
            self.node.param = self.param

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('statistic', 'time', 'instance', 'axis', 'lag', 'feature', 'space', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to apply filter to. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency'). Default: 'time'.")
        self.func_control = gui.comboBox(box, self, 'func', label='Func:', items=('boxcar', 'triang', 'blackman', 'hamming', 'hann', 'bartlett', 'flattop', 'parzen', 'bohman', 'blackmanharris', 'nuttall', 'barthann', 'kaiser', 'gaussian', 'slepian', 'chebwin'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('func'), tooltip="Type of window function to use. Default: 'hann'.")
        self.param_control = gui.lineEdit(box, self, 'param', label='Param:', orientation='horizontal', callback=lambda: self.property_changed('param'), tooltip="Window parameter. Needed for kaiser, gaussian, slepian, chebwin. Default: None.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
