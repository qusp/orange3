# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.filters import ImpedanceChannelRejection


class OWImpedanceChannelRejection(widget.OWWidget):
    name = "Impedance Channel Rejection"
    description = "Reject channels based on their impedance. Requires hardware support (e.g. Cognionics)."
    author = "Tim Mullen and Christian Kothe"
    icon = "icons/ImpedanceChannelRejection.svg"
    priority = 7
    category = "Filters"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    threshold = Setting(None)
    period = Setting(None)
    unit_conversion = Setting(None)
    calib_seconds = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = ImpedanceChannelRejection()
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

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.threshold_control = gui.lineEdit(box, self, 'threshold', 'Threshold:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('threshold'), tooltip="Impedance threshold (Mohms). Channels with impedance higher than this will be rejected.")
        self.period_control = gui.lineEdit(box, self, 'period', 'Period:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('period'), tooltip="Impedance signal period (samples).")
        self.unit_conversion_control = gui.lineEdit(box, self, 'unit_conversion', 'Unit conversion:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('unit_conversion'), tooltip="Factor for converting signal units to volts. This is usually taken care of by the data acquisition system.")
        self.calib_seconds_control = gui.lineEdit(box, self, 'calib_seconds', 'Calib seconds:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('calib_seconds'), tooltip="Minimum number of seconds used for calibration.")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

        # Set minimum width (in pixels).
        self.setMinimumWidth(480)

    def get_property_names(self):
        return list(self.node.ports(editable=True).keys())

    def get_property_control(self, name):
        return getattr(self, '{}_control'.format(name))

    def enable_property_control(self, name):
        self.get_property_control(name).setDisabled(False)

    def disable_property_control(self, name):
        self.get_property_control(name).setDisabled(True)

    def enable_property_controls(self, names=None):
        for name in (names or self.get_property_names()):
            self.enable_property_control(name)

    def disable_property_controls(self, names=None):
        for name in (names or self.get_property_names()):
            self.disable_property_control(name)

    def reset_default_properties(self, names=None):
        node = ImpedanceChannelRejection()

        for name in (names or self.get_property_names()):
            setattr(self.node, name, getattr(node, name))
            # Synchronize property changes back to the GUI.
            super().__setattr__(name, getattr(self.node, name))

    def property_changed(self, name):
        if self.last_error_caused_by and self.last_error_caused_by != name:
            return

        try:
            if self.node.port(name).value_type in (bool, str):
                value = getattr(self, name)
            else:
                # Evaluate string as pure Python code.
                content = getattr(self, name)
                try:
                    value = eval(content)
                except:
                    # take it as a literal string
                    print("Could not evaluate %s literally, "
                          "interpreting it as string." % content)
                    value = eval('"%s"' % content)

            setattr(self.node, name, value)
            # Synchronize property changes back to the GUI.
            super().__setattr__(name, getattr(self.node, name))

            if self.last_error_caused_by:
                self.last_error_caused_by = ''
                self.error()

            self.enable_property_controls()
            self.reset_button.setDisabled(False)
        except Exception as e:
            self.disable_property_controls()
            self.reset_button.setDisabled(True)
            self.enable_property_control(name)

            if not self.last_error_caused_by:
                self.last_error_caused_by = name

            self.error(text=str(e))

    def set_update(self, update):
        self.node.update = update

    def set_data(self, data):
        self.node.data = data


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ow = OWImpedanceChannelRejection()
    ow.show()
    app.exec_()