# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.spectral import SpectralSelection


class OWSpectralSelection(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Spectral Selection"
    description = "Restrict the spectrum of a segmented signal to a specified frequency range."
    author = "Christian Kothe"
    icon = "icons/SpectralSelection.svg"
    priority = 5
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
    frequencies = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(SpectralSelection())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('frequencies', self.node.frequencies)
        else:
            self.node.frequencies = self.frequencies

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.frequencies_control = gui.lineEdit(box, self, 'frequencies', 'Frequencies:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('frequencies'), tooltip="Frequency-domain selection, given as a list of [low, high] frequency band edges.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
