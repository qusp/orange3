# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.network import LSLOutput


class OWLSLOutput(cpewidget.CPEWidget):

    # Node meta-data.
    name = "LSL Output"
    description = "Send data to LSL"
    author = "Christian Kothe"
    icon = "icons/LSLOutput.svg"
    priority = 2
    category = "Network"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
    ]

    # Configuration properties.
    stream_name = Setting(None)
    stream_type = Setting(None)
    source_id = Setting(None)
    srate = Setting(None)
    chunk_len = Setting(None)
    max_buffered = Setting(None)
    only_signals = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(LSLOutput())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('stream_name', self.node.stream_name)
            super().__setattr__('stream_type', self.node.stream_type)
            super().__setattr__('source_id', self.node.source_id)
            super().__setattr__('srate', self.node.srate)
            super().__setattr__('chunk_len', self.node.chunk_len)
            super().__setattr__('max_buffered', self.node.max_buffered)
            super().__setattr__('only_signals', self.node.only_signals)
        else:
            self.node.stream_name = self.stream_name
            self.node.stream_type = self.stream_type
            self.node.source_id = self.source_id
            self.node.srate = self.srate
            self.node.chunk_len = self.chunk_len
            self.node.max_buffered = self.max_buffered
            self.node.only_signals = self.only_signals

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.stream_name_control = gui.lineEdit(box, self, 'stream_name', label='Stream name:', orientation='horizontal', callback=lambda: self.property_changed('stream_name'), tooltip="Name of output data stream. Data will be published in LSL under this name.")
        self.stream_type_control = gui.lineEdit(box, self, 'stream_type', label='Stream type:', orientation='horizontal', callback=lambda: self.property_changed('stream_type'), tooltip="Type of output data stream. Emitted data will have this content type.")
        self.source_id_control = gui.lineEdit(box, self, 'source_id', label='Source id:', orientation='horizontal', callback=lambda: self.property_changed('source_id'), tooltip="Source ID of the node. Assigning this allows other programs that receive this stream to auto-recover the connection if your program stops and gets restarted. For this to work, your id must be unique on your local network, and it must also be unchanged between restarts of your app.")
        self.srate_control = gui.lineEdit(box, self, 'srate', label='Srate:', orientation='horizontal', callback=lambda: self.property_changed('srate'), tooltip="Sampling rate override. Allows to override the nominal sampling rate.")
        self.chunk_len_control = gui.lineEdit(box, self, 'chunk_len', label='Chunk len:', orientation='horizontal', callback=lambda: self.property_changed('chunk_len'), tooltip="Output chunk length. Number of samples in emitted chunks. 0 = same as incoming.")
        self.max_buffered_control = gui.lineEdit(box, self, 'max_buffered', label='Max buffered:', orientation='horizontal', callback=lambda: self.property_changed('max_buffered'), tooltip="Preferred output buffer size. This much data will be buffered in case of network hitches.")
        self.only_signals_control = gui.checkBox(box, self, 'only_signals', label='Only signals', callback=lambda: self.property_changed('only_signals'), tooltip="Apply only to signal chunks. If unset, any numeric chunk data will be considered for sending; note, however, that there must only be one applicable chunk in the data.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
