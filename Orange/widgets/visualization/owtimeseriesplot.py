# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.visualization import TimeSeriesPlot


class OWTimeSeriesPlot(widget.OWWidget):
    name = "Time Series Plot"
    description = "Plot a multi-channel time series in real time."
    author = "Christian Kothe"
    icon = "icons/TimeSeriesPlot.svg"
    priority = 1
    category = "Visualization"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

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
        super().__init__()

        # Construct node instance and set default properties.
        self.node = TimeSeriesPlot()
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

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.scale_control = gui.lineEdit(box, self, 'scale', 'Scale:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('scale'))
        self.time_range_control = gui.lineEdit(box, self, 'time_range', 'Time range:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('time_range'))
        self.stream_name_control = gui.lineEdit(box, self, 'stream_name', 'Stream name:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('stream_name'))
        self.title_control = gui.lineEdit(box, self, 'title', 'Title:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('title'))
        self.background_color_control = gui.lineEdit(box, self, 'background_color', 'Background color:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('background_color'))
        self.line_color_control = gui.lineEdit(box, self, 'line_color', 'Line color:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('line_color'))
        self.zero_color_control = gui.lineEdit(box, self, 'zero_color', 'Zero color:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('zero_color'))
        self.antialiased_control = gui.checkBox(box, self, 'antialiased', 'Antialiased', callback=lambda: self.property_changed('antialiased'))
        self.downsampled_control = gui.checkBox(box, self, 'downsampled', 'Downsampled', callback=lambda: self.property_changed('downsampled'))
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

        # Set minimum width (in pixels).
        self.setMinimumWidth(480)

    def get_property_names(self):
        return list(self.node.ports(editable=True).keys())

    def get_property_control(self, name):
        return getattr(self, '{}_control'.format(name))

    def enable_property_control(self, name):
        self.get_property_control(name).setDisabled(False)

    def disable_property_control(self, name):
        self.get_property_control(name).setDisabled(True)

    def enable_property_controls(self, names=None):
        for name in (names or self.get_property_names()):
            self.enable_property_control(name)

    def disable_property_controls(self, names=None):
        for name in (names or self.get_property_names()):
            self.disable_property_control(name)

    def reset_default_properties(self, names=None):
        node = TimeSeriesPlot()

        for name in (names or self.get_property_names()):
            setattr(self.node, name, getattr(node, name))
            # Synchronize property changes back to the GUI.
            super().__setattr__(name, getattr(self.node, name))

    def property_changed(self, name):
        if self.last_error_caused_by and self.last_error_caused_by != name:
            return

        try:
            if self.node.port(name).value_type in (bool, str):
                value = getattr(self, name)
            else:
                # Evaluate string as pure Python code.
                value = eval(getattr(self, name))

            setattr(self.node, name, value)
            # Synchronize property changes back to the GUI.
            super().__setattr__(name, getattr(self.node, name))

            if self.last_error_caused_by:
                self.last_error_caused_by = ''
                self.error()

            self.enable_property_controls()
            self.reset_button.setDisabled(False)
        except Exception as e:
            self.disable_property_controls()
            self.reset_button.setDisabled(True)
            self.enable_property_control(name)

            if not self.last_error_caused_by:
                self.last_error_caused_by = name

            self.error(text=str(e))

    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWTimeSeriesPlot()
    ow.show()
    app.exec_()