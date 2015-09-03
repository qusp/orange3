# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.visualization import SpectrumPlot


class OWSpectrumPlot(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Spectrum Plot"
    description = "Plot multi-channel spectral data in real time."
    author = "Christian Kothe"
    icon = "icons/SpectrumPlot.svg"
    priority = 1
    category = "Visualization"

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
    scale = Setting(None)
    stream_name = Setting(None)
    stacked = Setting(None)
    title = Setting(None)
    background_color = Setting(None)
    line_color = Setting(None)
    zero_color = Setting(None)
    antialiased = Setting(None)
    downsampled = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SpectrumPlot())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('scale', self.node.scale)
            super().__setattr__('stream_name', self.node.stream_name)
            super().__setattr__('stacked', self.node.stacked)
            super().__setattr__('title', self.node.title)
            super().__setattr__('background_color', self.node.background_color)
            super().__setattr__('line_color', self.node.line_color)
            super().__setattr__('zero_color', self.node.zero_color)
            super().__setattr__('antialiased', self.node.antialiased)
            super().__setattr__('downsampled', self.node.downsampled)
        else:
            self.node.scale = self.scale
            self.node.stream_name = self.stream_name
            self.node.stacked = self.stacked
            self.node.title = self.title
            self.node.background_color = self.background_color
            self.node.line_color = self.line_color
            self.node.zero_color = self.zero_color
            self.node.antialiased = self.antialiased
            self.node.downsampled = self.downsampled

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.scale_control = gui.lineEdit(box, self, 'scale', label='Scale:', orientation='horizontal', callback=lambda: self.property_changed('scale'), tooltip="Data scale.")
        self.stream_name_control = gui.lineEdit(box, self, 'stream_name', label='Stream name:', orientation='horizontal', callback=lambda: self.property_changed('stream_name'), tooltip="Name of stream to display. Only streams whose name starts with this string are displayed.")
        self.stacked_control = gui.checkBox(box, self, 'stacked', label='Stacked', callback=lambda: self.property_changed('stacked'), tooltip="Display channels stacked.")
        self.title_control = gui.lineEdit(box, self, 'title', label='Title:', orientation='horizontal', callback=lambda: self.property_changed('title'), tooltip="Title of the plot.")
        self.background_color_control = gui.lineEdit(box, self, 'background_color', label='Background color:', orientation='horizontal', callback=lambda: self.property_changed('background_color'), tooltip="Background color. In hexadecimal notation (#RRGGBB).")
        self.line_color_control = gui.lineEdit(box, self, 'line_color', label='Line color:', orientation='horizontal', callback=lambda: self.property_changed('line_color'), tooltip="Color of the graph lines. In hexadecimal notation (#RRGGBB).")
        self.zero_color_control = gui.lineEdit(box, self, 'zero_color', label='Zero color:', orientation='horizontal', callback=lambda: self.property_changed('zero_color'), tooltip="Color of the zero line. In hexadecimal notation (#RRGGBBAA).")
        self.antialiased_control = gui.checkBox(box, self, 'antialiased', label='Antialiased', callback=lambda: self.property_changed('antialiased'), tooltip="Draw graphics antialiased. Can slow down plotting.")
        self.downsampled_control = gui.checkBox(box, self, 'downsampled', label='Downsampled', callback=lambda: self.property_changed('downsampled'), tooltip="Draw downsampled graphics. Can speed up plotting for dense time series.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
