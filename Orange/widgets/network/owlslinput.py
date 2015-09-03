# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.network import LSLInput


class OWLSLInput(cpewidget.CPEWidget):

    # Node meta-data.
    name = "LSL Input"
    description = "Receive data from LSL"
    author = "Christian Kothe"
    icon = "icons/LSLInput.svg"
    priority = 1
    category = "Network"

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
    query = Setting(None)
    marker_query = Setting(None)
    max_buflen = Setting(None)
    max_chunklen = Setting(None)
    max_blocklen = Setting(None)
    recover = Setting(None)
    channel_names = Setting(None)
    nominal_rate = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(LSLInput())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('query', self.node.query)
            super().__setattr__('marker_query', self.node.marker_query)
            super().__setattr__('max_buflen', self.node.max_buflen)
            super().__setattr__('max_chunklen', self.node.max_chunklen)
            super().__setattr__('max_blocklen', self.node.max_blocklen)
            super().__setattr__('recover', self.node.recover)
            super().__setattr__('channel_names', self.node.channel_names)
            super().__setattr__('nominal_rate', self.node.nominal_rate)
        else:
            self.node.query = self.query
            self.node.marker_query = self.marker_query
            self.node.max_buflen = self.max_buflen
            self.node.max_chunklen = self.max_chunklen
            self.node.max_blocklen = self.max_blocklen
            self.node.recover = self.recover
            self.node.channel_names = self.channel_names
            self.node.nominal_rate = self.nominal_rate

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.query_control = gui.lineEdit(box, self, 'query', 'Query:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('query'), tooltip="Query string to find a data stream. This is an LSL query (XPath predicate).")
        self.marker_query_control = gui.lineEdit(box, self, 'marker_query', 'Marker query:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('marker_query'), tooltip="Query string to find a marker stream. This is an LSL query (XPath predicate).")
        self.max_buflen_control = gui.lineEdit(box, self, 'max_buflen', 'Max buflen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_buflen'), tooltip="Maximum buffer length. This is the size of the network buffer to use, in s.")
        self.max_chunklen_control = gui.lineEdit(box, self, 'max_chunklen', 'Max chunklen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_chunklen'), tooltip="Maximum transmission chunk length. The preferred # of samples in chunks received from LSL.")
        self.max_blocklen_control = gui.lineEdit(box, self, 'max_blocklen', 'Max blocklen:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_blocklen'), tooltip="Maximum emitted block length. The preferred # of samples in blocks emitted by the node.")
        self.recover_control = gui.checkBox(box, self, 'recover', 'Recover', callback=lambda: self.property_changed('recover'), tooltip="Recover lost streams. Whether to attempt silent recovery of a lost LSL stream.")
        self.channel_names_control = gui.lineEdit(box, self, 'channel_names', 'Channel names:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('channel_names'), tooltip="Channel override. Allows to override the channel names of the data source.")
        self.nominal_rate_control = gui.lineEdit(box, self, 'nominal_rate', 'Nominal rate:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('nominal_rate'), tooltip="Sampling rate override. Allows to override the sampling rate of the data source.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update
