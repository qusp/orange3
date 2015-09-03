# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.spectral import MovingWindowMultitaperSpectrum


class OWMovingWindowMultitaperSpectrum(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Moving Window Multitaper Spectrum"
    description = "Calculate the power spectrum using the Multitaper method on a sliding window."
    author = "Christian Kothe"
    icon = "icons/MovingWindowMultitaperSpectrum.svg"
    priority = 2
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
    window_length = Setting(None)
    half_bandwidth = Setting(None)
    num_tapers = Setting(None)
    tapers = Setting(None)
    onesided = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(MovingWindowMultitaperSpectrum())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('window_length', self.node.window_length)
            super().__setattr__('half_bandwidth', self.node.half_bandwidth)
            super().__setattr__('num_tapers', self.node.num_tapers)
            super().__setattr__('tapers', self.node.tapers)
            super().__setattr__('onesided', self.node.onesided)
        else:
            self.node.window_length = self.window_length
            self.node.half_bandwidth = self.half_bandwidth
            self.node.num_tapers = self.num_tapers
            self.node.tapers = self.tapers
            self.node.onesided = self.onesided

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.window_length_control = gui.lineEdit(box, self, 'window_length', 'Window length:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window_length'), tooltip="Sliding window length in seconds.")
        self.half_bandwidth_control = gui.lineEdit(box, self, 'half_bandwidth', 'Half bandwidth:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('half_bandwidth'), tooltip="The spectral bandwidth (Hz) parameter.")
        self.num_tapers_control = gui.lineEdit(box, self, 'num_tapers', 'Num tapers:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_tapers'), tooltip="If the value is None, then we use the maximum number of tapers. For the DPSS tapers, this is 2*NW-1, where N is the window length and 2*W is the bandwidth.")
        self.tapers_control = gui.lineEdit(box, self, 'tapers', 'Tapers:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tapers'), tooltip="A matrix of tapering windows. Optional; if not given, tapers will be computed by dpss.")
        self.onesided_control = gui.checkBox(box, self, 'onesided', 'Onesided', callback=lambda: self.property_changed('onesided'), tooltip="Return one-sided spectrum. For complex data, the spectrum is always two-sided. Default: True.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
