# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.fileio import PlayBackREC


class OWPlayBackREC(cpewidget.CPEWidget):

    # Node meta-data.
    name = "LoadFromFile"
    description = "Retrieve the next data packet from a file using pickle."
    author = "Alejandro Ojeda"
    icon = "icons/PlayBackREC.svg"
    priority = 3
    category = "Fileio"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    filename = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(PlayBackREC())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('filename', self.node.filename)
        else:
            self.node.filename = self.filename

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.filename_control = gui.lineEdit(box, self, 'filename', label='Filename:', orientation='horizontal', callback=lambda: self.property_changed('filename'), tooltip="Name of the file where the packets will be saved.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update
