# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.formatting import StreamData


class OWStreamData(widget.OWWidget):
    name = "Stream Data"
    description = "Stream pre-recorded data at a particular rate."
    author = "Christian Kothe"
    icon = "icons/StreamData.svg"
    priority = 2
    category = "Formatting"

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

    timing = Setting(None)
    speedup = Setting(None)
    update_interval = Setting(None)
    jitter_percent = Setting(None)
    randseed = Setting(None)
    hitch_probability = Setting(None)
    looping = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = StreamData()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('timing', self.node.timing)
            super().__setattr__('speedup', self.node.speedup)
            super().__setattr__('update_interval', self.node.update_interval)
            super().__setattr__('jitter_percent', self.node.jitter_percent)
            super().__setattr__('randseed', self.node.randseed)
            super().__setattr__('hitch_probability', self.node.hitch_probability)
            super().__setattr__('looping', self.node.looping)
        else:
            self.node.timing = self.timing
            self.node.speedup = self.speedup
            self.node.update_interval = self.update_interval
            self.node.jitter_percent = self.jitter_percent
            self.node.randseed = self.randseed
            self.node.hitch_probability = self.hitch_probability
            self.node.looping = self.looping

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.timing_control = gui.lineEdit(box, self, 'timing', 'Timing:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('timing'), tooltip="Timing source. Can be either 'wallclock', in which case the data is streamed at a particular factor of real time (e.g., 1x) based on the wall-clock time, or 'deterministic', in which case the data is streamed out in chunks of a particular pre-determined length (e.g., 32 samples per chunk). The deterministic mode is primarily useful for debugging.")
        self.speedup_control = gui.lineEdit(box, self, 'speedup', 'Speedup:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('speedup'), tooltip="Wall-clock data rate factor. This is the data rate factor relative to real time (e.g. 2 means that the data plays back at 2x real time).")
        self.update_interval_control = gui.lineEdit(box, self, 'update_interval', 'Update interval:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('update_interval'), tooltip="Deterministic update interval. This is the approx duration of each emitted chunk.")
        self.jitter_percent_control = gui.lineEdit(box, self, 'jitter_percent', 'Jitter percent:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('jitter_percent'), tooltip="Deterministic update jitter. This is the jitter, in percent, that is applied to the update interval. Corresponds to 1 standard deviation of a Gaussian distribution.")
        self.randseed_control = gui.lineEdit(box, self, 'randseed', 'Randseed:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('randseed'), tooltip="Deterministic random seed. This is the random seed that can be used to yield different execution traces.")
        self.hitch_probability_control = gui.lineEdit(box, self, 'hitch_probability', 'Hitch probability:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('hitch_probability'), tooltip="Probability of simulated hitches. In Percent. A hitch is an occasional empty packet.")
        self.looping_control = gui.checkBox(box, self, 'looping', 'Looping', callback=lambda: self.property_changed('looping'), tooltip="Looping playback. Whether to stream the data in a loop.")
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
        node = StreamData()

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
    ow = OWStreamData()
    ow.show()
    app.exec_()