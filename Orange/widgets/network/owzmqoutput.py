# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.network import ZMQOutput


class OWZMQOutput(cpewidget.CPEWidget):

    # Node meta-data.
    name = "ZMQ Output"
    description = "Write outgoing messages to a connected ZeroMQ socket"
    author = "Aaron McCoy"
    icon = "icons/ZMQOutput.svg"
    priority = 4
    category = "Network"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': builtins.object, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
    ]

    # Configuration properties.
    endpoint = Setting(None)
    encoding = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ZMQOutput())

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
        self.endpoint_control = gui.lineEdit(box, self, 'endpoint', label='Endpoint:', orientation='horizontal', callback=lambda: self.property_changed('endpoint'), tooltip="Endpoint on which to connect the ZeroMQ socket to write outgoing messages. This is specified as a unique combination of protocol, host and port. For more information, see the ZeroMQ documentation.")
        self.encoding_control = gui.comboBox(box, self, 'encoding', label='Encoding:', items=('bytes', 'json', 'msgpack', 'pickle', 'string'), sendSelectedValue=True, orientation='horizontal', callback=lambda: self.property_changed('encoding'), tooltip="Encoding type. Messages written to the connected ZeroMQ socket are encoded based on the value of this setting.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
