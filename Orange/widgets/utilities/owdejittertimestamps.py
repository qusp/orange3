# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import DejitterTimestamps


class OWDejitterTimestamps(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Dejitter Timestamps"
    description = "De-jitter the time-stamps of the given streams. This removes any jitter from the time-stamps using a high-quality method (RLS)."
    author = "Christian Kothe"
    icon = "icons/DejitterTimestamps.svg"
    priority = 5
    category = "Utilities"

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
    forget_halftime = Setting(None)
    warmup_samples = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(DejitterTimestamps())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('forget_halftime', self.node.forget_halftime)
            super().__setattr__('warmup_samples', self.node.warmup_samples)
        else:
            self.node.forget_halftime = self.forget_halftime
            self.node.warmup_samples = self.warmup_samples

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.forget_halftime_control = gui.lineEdit(box, self, 'forget_halftime', 'Forget halftime:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('forget_halftime'), tooltip="Forget factor as information half-life. In estimating the effective sampling rate a sample which is this many seconds old will be weighted 1/2 as much as the current sample in an exponentially decaying window.")
        self.warmup_samples_control = gui.lineEdit(box, self, 'warmup_samples', 'Warmup samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('warmup_samples'), tooltip="Warmup samples. The number of samples for which we warm up the timing statistics. The first few samples will be updated in a block manner, followed by regular samplewise updates.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
