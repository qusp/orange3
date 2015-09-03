# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.formatting import StreamData


class OWStreamData(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Stream Data"
    description = "Stream pre-recorded data at a particular rate."
    author = "Christian Kothe"
    icon = "icons/StreamData.svg"
    priority = 2
    category = "Formatting"

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
    timing = Setting(None)
    speedup = Setting(None)
    update_interval = Setting(None)
    jitter_percent = Setting(None)
    randseed = Setting(None)
    hitch_probability = Setting(None)
    looping = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(StreamData())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('timing', self.node.timing)
            super().__setattr__('speedup', self.node.speedup)
            super().__setattr__('update_interval', self.node.update_interval)
            super().__setattr__('jitter_percent', self.node.jitter_percent)
            super().__setattr__('randseed', self.node.randseed)
            super().__setattr__('hitch_probability', self.node.hitch_probability)
            super().__setattr__('looping', self.node.looping)
        else:
            self.node.timing = self.timing
            self.node.speedup = self.speedup
            self.node.update_interval = self.update_interval
            self.node.jitter_percent = self.jitter_percent
            self.node.randseed = self.randseed
            self.node.hitch_probability = self.hitch_probability
            self.node.looping = self.looping

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.timing_control = gui.lineEdit(box, self, 'timing', 'Timing:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('timing'), tooltip="Timing source. Can be either 'wallclock', in which case the data is streamed at a particular factor of real time (e.g., 1x) based on the wall-clock time, or 'deterministic', in which case the data is streamed out in chunks of a particular pre-determined length (e.g., 32 samples per chunk). The deterministic mode is primarily useful for debugging.")
        self.speedup_control = gui.lineEdit(box, self, 'speedup', 'Speedup:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('speedup'), tooltip="Wall-clock data rate factor. This is the data rate factor relative to real time (e.g. 2 means that the data plays back at 2x real time).")
        self.update_interval_control = gui.lineEdit(box, self, 'update_interval', 'Update interval:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('update_interval'), tooltip="Deterministic update interval. This is the approx duration of each emitted chunk.")
        self.jitter_percent_control = gui.lineEdit(box, self, 'jitter_percent', 'Jitter percent:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('jitter_percent'), tooltip="Deterministic update jitter. This is the jitter, in percent, that is applied to the update interval. Corresponds to 1 standard deviation of a Gaussian distribution.")
        self.randseed_control = gui.lineEdit(box, self, 'randseed', 'Randseed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('randseed'), tooltip="Deterministic random seed. This is the random seed that can be used to yield different execution traces.")
        self.hitch_probability_control = gui.lineEdit(box, self, 'hitch_probability', 'Hitch probability:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('hitch_probability'), tooltip="Probability of simulated hitches. In Percent. A hitch is an occasional empty packet.")
        self.looping_control = gui.checkBox(box, self, 'looping', 'Looping', callback=lambda: self.property_changed('looping'), tooltip="Looping playback. Whether to stream the data in a loop.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
