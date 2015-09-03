# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.spectral import Coherence


class OWCoherence(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Coherence"
    description = "Calculate the spectral coherence between all pairs of channels using the Welch method."
    author = "Christian Kothe"
    icon = "icons/Coherence.svg"
    priority = 1
    category = "Spectral"

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
    segment_samples = Setting(None)
    overlap_samples = Setting(None)
    window = Setting(None)
    detrend = Setting(None)
    onesided = Setting(None)
    fft_size = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(Coherence())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('segment_samples', self.node.segment_samples)
            super().__setattr__('overlap_samples', self.node.overlap_samples)
            super().__setattr__('window', self.node.window)
            super().__setattr__('detrend', self.node.detrend)
            super().__setattr__('onesided', self.node.onesided)
            super().__setattr__('fft_size', self.node.fft_size)
        else:
            self.node.segment_samples = self.segment_samples
            self.node.overlap_samples = self.overlap_samples
            self.node.window = self.window
            self.node.detrend = self.detrend
            self.node.onesided = self.onesided
            self.node.fft_size = self.fft_size

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.segment_samples_control = gui.lineEdit(box, self, 'segment_samples', label='Segment samples:', orientation='horizontal', callback=lambda: self.property_changed('segment_samples'), tooltip="Segment length. In samples.")
        self.overlap_samples_control = gui.lineEdit(box, self, 'overlap_samples', label='Overlap samples:', orientation='horizontal', callback=lambda: self.property_changed('overlap_samples'), tooltip="Number of overlapped samples. If None, defaults to half of segment_samples.")
        self.window_control = gui.comboBox(box, self, 'window', label='Window:', items=('boxcar', 'triang', 'blackman', 'hamming', 'hann', 'bartlett', 'flattop', 'parzen', 'bohman', 'blackmanharris', 'nuttall', 'barthann', 'kaiser', 'gaussian', 'slepian', 'chebwin'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('window'), tooltip="Type of window function to use.")
        self.detrend_control = gui.comboBox(box, self, 'detrend', label='Detrend:', items=('constant', 'linear'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('detrend'), tooltip="Detrending method.")
        self.onesided_control = gui.checkBox(box, self, 'onesided', label='Onesided', callback=lambda: self.property_changed('onesided'), tooltip="Return one-sided spectrum. For complex data, the spectrum is always two-sided.")
        self.fft_size_control = gui.lineEdit(box, self, 'fft_size', label='Fft size:', orientation='horizontal', callback=lambda: self.property_changed('fft_size'), tooltip="Length of the FFT used, if a zero padded FFT is desired.  If None,  the FFT length equals segment_samples.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
