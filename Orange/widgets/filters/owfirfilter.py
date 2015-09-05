# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import FIRFilter


class OWFIRFilter(cpewidget.CPEWidget):

    # Node meta-data.
    name = "FIR Filter"
    description = "Apply FIR filter to data. This node is used to implement frequency filtering, for instance to realize low-pass, high-pass, band-pass, or band-stop filters. When band edges lie in low frequencies (under 5 Hz) then the filter will incur a substantial delay unless the minimum_phase option is enabled. Also, this filter is rather slow when long kernels are applied to long signals."
    author = "Christian Kothe"
    icon = "icons/FIRFilter.svg"
    priority = 4
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
    order = Setting(None)
    frequencies = Setting(None)
    mode = Setting(None)
    antisymmetric = Setting(None)
    minimum_phase = Setting(None)
    stop_atten = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(FIRFilter())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('order', self.node.order)
            super().__setattr__('frequencies', self.node.frequencies)
            super().__setattr__('mode', self.node.mode)
            super().__setattr__('antisymmetric', self.node.antisymmetric)
            super().__setattr__('minimum_phase', self.node.minimum_phase)
            super().__setattr__('stop_atten', self.node.stop_atten)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.axis = self.axis
            self.node.order = self.order
            self.node.frequencies = self.frequencies
            self.node.mode = self.mode
            self.node.antisymmetric = self.antisymmetric
            self.node.minimum_phase = self.minimum_phase
            self.node.stop_atten = self.stop_atten
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.comboBox(box, self, 'axis', label='Axis:', items=('frequency', 'instance', 'feature', 'space', 'axis', 'lag', 'statistic', 'time'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('axis'), tooltip="Axis to apply filter to. This is a string that identifies the axis to use (e.g. 'time', 'space', 'frequency'). Default: 'time'.")
        self.order_control = gui.lineEdit(box, self, 'order', label='Order:', orientation='horizontal', callback=lambda: self.property_changed('order'), tooltip="Filter order. If unspecified, will be auto-determined based on stop_atten using the Kaiser window rule.")
        self.frequencies_control = gui.lineEdit(box, self, 'frequencies', label='Frequencies:', orientation='horizontal', callback=lambda: self.property_changed('frequencies'), tooltip="Frequency band edges. For low/highpass mode, this is [f1, f2] in Hz, for bandpass/stop it is [f1,f2,f3,f4], and for freeform it is [(0,g0),(f1,g1),(f2,g2),...,(-1,gn)] where gn is the gain at frequency n, and a frequency of -1 is replaced by the signal's Nyquist frequency.")
        self.mode_control = gui.comboBox(box, self, 'mode', label='Mode:', items=('lowpass', 'highpass', 'bandpass', 'bandstop', 'freeform'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('mode'), tooltip="Filter mode.")
        self.antisymmetric_control = gui.checkBox(box, self, 'antisymmetric', label='Antisymmetric', callback=lambda: self.property_changed('antisymmetric'), tooltip="Design antisymmetric filter. See description for more details. Default: False.")
        self.minimum_phase_control = gui.checkBox(box, self, 'minimum_phase', label='Minimum phase', callback=lambda: self.property_changed('minimum_phase'), tooltip="Design minimum-phase filter. Minimizes the latency of the filter.")
        self.stop_atten_control = gui.lineEdit(box, self, 'stop_atten', label='Stop atten:', orientation='horizontal', callback=lambda: self.property_changed('stop_atten'), tooltip="Minimum attenuation in stop-band. In dB. Default: 30.0.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any numeric chunk data will be filtered. Default: True.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
