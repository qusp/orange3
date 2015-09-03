# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import InjectCalibrationData


class OWInjectCalibrationData(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Inject Calibration Data"
    description = "Inject Calibration Data into the stream.."
    author = "Christian Kothe"
    icon = "icons/InjectCalibrationData.svg"
    priority = 9
    category = "Utilities"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Streaming Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_streaming_data', 'flags': 0},
        {'name': 'Calib Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_calib_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(InjectCalibrationData())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            pass
        else:
            pass

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_streaming_data(self, streaming_data):
        self.node.streaming_data = streaming_data

    def set_calib_data(self, calib_data):
        self.node.calib_data = calib_data
