# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import DejitterTimestamps


class OWDejitterTimestamps(widget.OWWidget):
    name = "Dejitter Timestamps"
    description = "De-jitter the time-stamps of the given streams. This removes any jitter from the time-stamps using a high-quality method (RLS)."
    author = "Christian Kothe"
    icon = "icons/DejitterTimestamps.svg"
    priority = 5
    category = "Utilities"

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

    forget_halftime = Setting(None)
    warmup_samples = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = DejitterTimestamps()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('forget_halftime', self.node.forget_halftime)
            super().__setattr__('warmup_samples', self.node.warmup_samples)
        else:
            self.node.forget_halftime = self.forget_halftime
            self.node.warmup_samples = self.warmup_samples

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.forget_halftime_control = gui.lineEdit(box, self, 'forget_halftime', 'Forget halftime:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('forget_halftime'), tooltip="Forget factor as information half-life. In estimating the effective sampling rate a sample which is this many seconds old will be weighted 1/2 as much as the current sample in an exponentially decaying window.")
        self.warmup_samples_control = gui.lineEdit(box, self, 'warmup_samples', 'Warmup samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('warmup_samples'), tooltip="Warmup samples. The number of samples for which we warm up the timing statistics. The first few samples will be updated in a block manner, followed by regular samplewise updates.")
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
        node = DejitterTimestamps()

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
    ow = OWDejitterTimestamps()
    ow.show()
    app.exec_()