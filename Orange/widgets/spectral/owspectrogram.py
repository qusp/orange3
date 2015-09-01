# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.spectral import Spectrogram


class OWSpectrogram(widget.OWWidget):
    name = "Spectrogram"
    description = "Calculate a spectrogram (time/frequency representation)."
    author = "Christian Kothe"
    icon = "icons/Spectrogram.svg"
    priority = 6
    category = "Spectral"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    want_main_area = False

    segment_samples = Setting(None)
    overlap_samples = Setting(None)
    scaling = Setting(None)
    window = Setting(None)
    fft_size = Setting(None)
    detrend = Setting(None)
    onesided = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = Spectrogram()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('segment_samples', self.node.segment_samples)
            super().__setattr__('overlap_samples', self.node.overlap_samples)
            super().__setattr__('scaling', self.node.scaling)
            super().__setattr__('window', self.node.window)
            super().__setattr__('fft_size', self.node.fft_size)
            super().__setattr__('detrend', self.node.detrend)
            super().__setattr__('onesided', self.node.onesided)
        else:
            self.node.segment_samples = self.segment_samples
            self.node.overlap_samples = self.overlap_samples
            self.node.scaling = self.scaling
            self.node.window = self.window
            self.node.fft_size = self.fft_size
            self.node.detrend = self.detrend
            self.node.onesided = self.onesided

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.segment_samples_control = gui.lineEdit(box, self, 'segment_samples', 'Segment samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('segment_samples'))
        self.overlap_samples_control = gui.lineEdit(box, self, 'overlap_samples', 'Overlap samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('overlap_samples'))
        self.scaling_control = gui.lineEdit(box, self, 'scaling', 'Scaling:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('scaling'))
        self.window_control = gui.lineEdit(box, self, 'window', 'Window:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window'))
        self.fft_size_control = gui.lineEdit(box, self, 'fft_size', 'Fft size:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('fft_size'))
        self.detrend_control = gui.lineEdit(box, self, 'detrend', 'Detrend:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('detrend'))
        self.onesided_control = gui.checkBox(box, self, 'onesided', 'Onesided', callback=lambda: self.property_changed('onesided'))
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
        node = Spectrogram()

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
                value = eval(getattr(self, name))

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
    ow = OWSpectrogram()
    ow.show()
    app.exec_()