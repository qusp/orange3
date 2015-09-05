# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import OverrideTimestamps


class OWOverrideTimestamps(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Override Timestamps"
    description = "Override time stamps based on the sampling rate of the stream."
    author = "Christian Kothe (ckothe@ucsd.edu)"
    icon = "icons/OverrideTimestamps.svg"
    priority = 12
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
    timebase = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(OverrideTimestamps())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('timebase', self.node.timebase)
        else:
            self.node.timebase = self.timebase

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.timebase_control = gui.comboBox(box, self, 'timebase', label='Timebase:', items=('wallclock', 'abstract'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('timebase'), tooltip="Time base to use. The wallclock setting will allow to approximately synchronize multiple streams, but has jitter that needs to be corrected prior to using certain other filters. The abstract setting is monotonic and has no jitter, but each stream has its own clock domain, so they cannot be aligned based on time stamps, not even approximately.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
