# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.fileio import RecordToREC


class OWRecordToREC(cpewidget.CPEWidget):

    # Node meta-data.
    name = "RecordToREC"
    description = "Record data packets to .rec file."
    author = "Alejandro Ojeda"
    icon = "icons/RecordToREC.svg"
    priority = 4
    category = "Fileio"

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
    filename = Setting(None)
    protocol_ver = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(RecordToREC())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('filename', self.node.filename)
            super().__setattr__('protocol_ver', self.node.protocol_ver)
        else:
            self.node.filename = self.filename
            self.node.protocol_ver = self.protocol_ver

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.filename_control = gui.lineEdit(box, self, 'filename', 'Filename:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('filename'), tooltip="Name of the file where the packets will be saved.")
        self.protocol_ver_control = gui.lineEdit(box, self, 'protocol_ver', 'Protocol ver:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('protocol_ver'), tooltip="Pickle protocol version.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
