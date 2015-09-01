# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
from neuropype.nodes.spectral import WelchSpectrum


class OWWelchSpectrum(widget.OWWidget):
    name = 'Welch Spectrum'
    description = 'Calculate the power spectrum using the Welch method.'
    author = 'Christian Kothe'
    icon = 'icons/WelchSpectrum.svg'
    priority = 7
    category = 'Spectral'

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

    axis = Setting(None)
    segment_samples = Setting(None)
    overlap_samples = Setting(None)
    window = Setting(None)
    detrend = Setting(None)
    onesided = Setting(None)
    scaling = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = WelchSpectrum()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('axis', self.node.axis)
            super().__setattr__('segment_samples', self.node.segment_samples)
            super().__setattr__('overlap_samples', self.node.overlap_samples)
            super().__setattr__('window', self.node.window)
            super().__setattr__('detrend', self.node.detrend)
            super().__setattr__('onesided', self.node.onesided)
            super().__setattr__('scaling', self.node.scaling)
        else:
            self.node.axis = self.axis
            self.node.segment_samples = self.segment_samples
            self.node.overlap_samples = self.overlap_samples
            self.node.window = self.window
            self.node.detrend = self.detrend
            self.node.onesided = self.onesided
            self.node.scaling = self.scaling

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.axis_control = gui.lineEdit(box, self, 'axis', 'Axis:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('axis'))
        self.segment_samples_control = gui.lineEdit(box, self, 'segment_samples', 'Segment samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('segment_samples'))
        self.overlap_samples_control = gui.lineEdit(box, self, 'overlap_samples', 'Overlap samples:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('overlap_samples'))
        self.window_control = gui.lineEdit(box, self, 'window', 'Window:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('window'))
        self.detrend_control = gui.lineEdit(box, self, 'detrend', 'Detrend:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('detrend'))
        self.onesided_control = gui.checkBox(box, self, 'onesided', 'Onesided', callback=lambda: self.property_changed('onesided'))
        self.scaling_control = gui.lineEdit(box, self, 'scaling', 'Scaling:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('scaling'))
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
        node = WelchSpectrum()

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
    ow = OWWelchSpectrum()
    ow.show()
    app.exec_()