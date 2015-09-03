# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import ImpedanceChannelRejection


class OWImpedanceChannelRejection(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Impedance Channel Rejection"
    description = "Reject channels based on their impedance. Requires hardware support (e.g. Cognionics)."
    author = "Tim Mullen and Christian Kothe"
    icon = "icons/ImpedanceChannelRejection.svg"
    priority = 7
    category = "Filters"

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
    threshold = Setting(None)
    period = Setting(None)
    unit_conversion = Setting(None)
    calib_seconds = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ImpedanceChannelRejection())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('threshold', self.node.threshold)
            super().__setattr__('period', self.node.period)
            super().__setattr__('unit_conversion', self.node.unit_conversion)
            super().__setattr__('calib_seconds', self.node.calib_seconds)
        else:
            self.node.threshold = self.threshold
            self.node.period = self.period
            self.node.unit_conversion = self.unit_conversion
            self.node.calib_seconds = self.calib_seconds

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.threshold_control = gui.lineEdit(box, self, 'threshold', 'Threshold:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('threshold'), tooltip="Impedance threshold (Mohms). Channels with impedance higher than this will be rejected.")
        self.period_control = gui.lineEdit(box, self, 'period', 'Period:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('period'), tooltip="Impedance signal period (samples).")
        self.unit_conversion_control = gui.lineEdit(box, self, 'unit_conversion', 'Unit conversion:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('unit_conversion'), tooltip="Factor for converting signal units to volts. This is usually taken care of by the data acquisition system.")
        self.calib_seconds_control = gui.lineEdit(box, self, 'calib_seconds', 'Calib seconds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('calib_seconds'), tooltip="Minimum number of seconds used for calibration.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data
