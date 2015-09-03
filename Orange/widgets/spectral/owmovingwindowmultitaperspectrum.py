# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.spectral import MovingWindowMultitaperSpectrum


class OWMovingWindowMultitaperSpectrum(widget.OWWidget):
    name = "Moving Window Multitaper Spectrum"
    description = "Calculate the power spectrum using the Multitaper method on a sliding window."
    author = "Christian Kothe"
    icon = "icons/MovingWindowMultitaperSpectrum.svg"
    priority = 2
    category = "Spectral"

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

    window_length = Setting(None)
    half_bandwidth = Setting(None)
    num_tapers = Setting(None)
    tapers = Setting(None)
    onesided = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = MovingWindowMultitaperSpectrum()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('window_length', self.node.window_length)
            super().__setattr__('half_bandwidth', self.node.half_bandwidth)
            super().__setattr__('num_tapers', self.node.num_tapers)
            super().__setattr__('tapers', self.node.tapers)
            super().__setattr__('onesided', self.node.onesided)
        else:
            self.node.window_length = self.window_length
            self.node.half_bandwidth = self.half_bandwidth
            self.node.num_tapers = self.num_tapers
            self.node.tapers = self.tapers
            self.node.onesided = self.onesided

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.window_length_control = gui.lineEdit(box, self, 'window_length', 'Window length:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window_length'), tooltip="Sliding window length in seconds.")
        self.half_bandwidth_control = gui.lineEdit(box, self, 'half_bandwidth', 'Half bandwidth:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('half_bandwidth'), tooltip="The spectral bandwidth (Hz) parameter.")
        self.num_tapers_control = gui.lineEdit(box, self, 'num_tapers', 'Num tapers:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('num_tapers'), tooltip="If the value is None, then we use the maximum number of tapers. For the DPSS tapers, this is 2*NW-1, where N is the window length and 2*W is the bandwidth.")
        self.tapers_control = gui.lineEdit(box, self, 'tapers', 'Tapers:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('tapers'), tooltip="A matrix of tapering windows. Optional; if not given, tapers will be computed by dpss.")
        self.onesided_control = gui.checkBox(box, self, 'onesided', 'Onesided', callback=lambda: self.property_changed('onesided'), tooltip="Return one-sided spectrum. For complex data, the spectrum is always two-sided. Default: True.")
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
        node = MovingWindowMultitaperSpectrum()

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
    ow = OWMovingWindowMultitaperSpectrum()
    ow.show()
    app.exec_()