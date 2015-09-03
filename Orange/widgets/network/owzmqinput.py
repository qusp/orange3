# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.network import ZMQInput


class OWZMQInput(cpewidget.CPEWidget):

    # Node meta-data.
    name = "ZMQ Input"
    description = "Read incoming messages from a bound ZeroMQ socket"
    author = "Aaron McCoy"
    icon = "icons/ZMQInput.svg"
    priority = 3
    category = "Network"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': builtins.object, 'flags': 0},
    ]

    # Configuration properties.
    endpoint = Setting(None)
    encoding = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ZMQInput())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('endpoint', self.node.endpoint)
            super().__setattr__('encoding', self.node.encoding)
        else:
            self.node.endpoint = self.endpoint
            self.node.encoding = self.encoding

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.endpoint_control = gui.lineEdit(box, self, 'endpoint', label='Endpoint:', orientation='horizontal', callback=lambda: self.property_changed('endpoint'), tooltip="Endpoint on which to bind the ZeroMQ socket to listen for incoming messages to read. This is specified as a unique combination of protocol, host and port. For more information, see the ZeroMQ documentation.")
        self.encoding_control = gui.comboBox(box, self, 'encoding', label='Encoding:', items=('bytearray', 'bytes', 'json', 'msgpack', 'pickle', 'string'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('encoding'), tooltip="Encoding type. Messages read from the bound ZeroMQ socket are decoded based on the value of this setting.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update
