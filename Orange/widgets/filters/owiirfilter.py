# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import IIRFilter


class OWIIRFilter(cpewidget.CPEWidget):

    # Node meta-data.
    name = "IIR Filter"
    description = "Apply IIR filter to data. See also scipy.signal.iirdesign."
    author = "Christian Kothe"
    icon = "icons/IIRFilter.svg"
    priority = 6
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
    frequencies = Setting(None)
    mode = Setting(None)
    design = Setting(None)
    pass_loss = Setting(None)
    stop_atten = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(IIRFilter())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('frequencies', self.node.frequencies)
            super().__setattr__('mode', self.node.mode)
            super().__setattr__('design', self.node.design)
            super().__setattr__('pass_loss', self.node.pass_loss)
            super().__setattr__('stop_atten', self.node.stop_atten)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.axis = self.axis
            self.node.frequencies = self.frequencies
            self.node.mode = self.mode
            self.node.design = self.design
            self.node.pass_loss = self.pass_loss
            self.node.stop_atten = self.stop_atten
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('statistic', 'time', 'instance', 'axis', 'lag', 'feature', 'space', 'frequency'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to apply filter to. This is a string that identifies the axis to use (e.g., 'time', 'space', 'frequency'). Default: 'time'.")
        self.frequencies_control = gui.lineEdit(box, self, 'frequencies', label='Frequencies:', orientation='horizontal', callback=lambda: self.property_changed('frequencies'), tooltip="Transition frequencies. The values in freq must be nondecreasing. For a low/high-pass filter, this is: [transition-start, transition-end], in Hz. For a band-pass/stop filter, this is: [low-transition-start, low-transition-end, hi-transition-start, hi-transition-end], in Hz. Default: None.")
        self.mode_control = gui.comboBox(box, self, 'mode', label='Mode:', items=('lowpass', 'highpass', 'bandpass', 'bandstop'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('mode'), tooltip="Filter mode. Default: 'bandpass'.")
        self.design_control = gui.comboBox(box, self, 'design', label='Design:', items=('butter', 'cheby1', 'cheby2', 'ellip', 'bessel'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('design'), tooltip="Filter design. This the the filter design rule to use. Default: 'butter'.")
        self.pass_loss_control = gui.lineEdit(box, self, 'pass_loss', label='Pass loss:', orientation='horizontal', callback=lambda: self.property_changed('pass_loss'), tooltip="Maximum loss in pass-band. In dB. Default: 3.0.")
        self.stop_atten_control = gui.lineEdit(box, self, 'stop_atten', label='Stop atten:', orientation='horizontal', callback=lambda: self.property_changed('stop_atten'), tooltip="Minimum attenuation in stop-band. In dB. Default: 40.0.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any numeric chunk data will be filtered. Default: True.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
