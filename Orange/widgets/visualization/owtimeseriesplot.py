# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.visualization import TimeSeriesPlot


class OWTimeSeriesPlot(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Time Series Plot"
    description = "Plot a multi-channel time series in real time."
    author = "Christian Kothe"
    icon = "icons/TimeSeriesPlot.svg"
    priority = 2
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
    time_range = Setting(None)
    stream_name = Setting(None)
    title = Setting(None)
    background_color = Setting(None)
    line_color = Setting(None)
    zero_color = Setting(None)
    antialiased = Setting(None)
    downsampled = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(TimeSeriesPlot())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('scale', self.node.scale)
            super().__setattr__('time_range', self.node.time_range)
            super().__setattr__('stream_name', self.node.stream_name)
            super().__setattr__('title', self.node.title)
            super().__setattr__('background_color', self.node.background_color)
            super().__setattr__('line_color', self.node.line_color)
            super().__setattr__('zero_color', self.node.zero_color)
            super().__setattr__('antialiased', self.node.antialiased)
            super().__setattr__('downsampled', self.node.downsampled)
        else:
            self.node.scale = self.scale
            self.node.time_range = self.time_range
            self.node.stream_name = self.stream_name
            self.node.title = self.title
            self.node.background_color = self.background_color
            self.node.line_color = self.line_color
            self.node.zero_color = self.zero_color
            self.node.antialiased = self.antialiased
            self.node.downsampled = self.downsampled

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.scale_control = gui.lineEdit(box, self, 'scale', 'Scale:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('scale'), tooltip="Data scale.")
        self.time_range_control = gui.lineEdit(box, self, 'time_range', 'Time range:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('time_range'), tooltip="Time range to display. This is the number of seconds of recent data that shall be plotted.")
        self.stream_name_control = gui.lineEdit(box, self, 'stream_name', 'Stream name:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('stream_name'), tooltip="Name of stream to display. Only streams whose name starts with this string are displayed.")
        self.title_control = gui.lineEdit(box, self, 'title', 'Title:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('title'), tooltip="Title of the plot.")
        self.background_color_control = gui.lineEdit(box, self, 'background_color', 'Background color:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('background_color'), tooltip="Background color. In hexadecimal notation (#RRGGBB).")
        self.line_color_control = gui.lineEdit(box, self, 'line_color', 'Line color:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('line_color'), tooltip="Color of the graph lines. In hexadecimal notation (#RRGGBB).")
        self.zero_color_control = gui.lineEdit(box, self, 'zero_color', 'Zero color:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('zero_color'), tooltip="Color of the zero line.")
        self.antialiased_control = gui.checkBox(box, self, 'antialiased', 'Antialiased', callback=lambda: self.property_changed('antialiased'), tooltip="Draw graphics antialiased. Can slow down plotting.")
        self.downsampled_control = gui.checkBox(box, self, 'downsampled', 'Downsampled', callback=lambda: self.property_changed('downsampled'), tooltip="Draw downsampled graphics. Can speed up plotting for dense time series.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
