# -*- coding: utf-8 -*-

import builtins
import sys

from PyQt4 import QtGui

from Orange.widgets import widget, gui
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.utilities import BatchPackets


class OWBatchPackets(widget.OWWidget):
    name = "Merge Successive Packets"
    description = "Merges successive packets to maintain real-time rates. Normally, the pipeline is driven by input plugins that output all data since the last update, which naturally increases the chunk size if necessary to maintain real-time rates. However, when the pipeline is driven with a fixed chunk size that is too small for real time, this node can be inserted to merge successive  chunks (actually packets) in order to achieve real-time behavior."
    author = "Christian Kothe"
    icon = "icons/BatchPackets.svg"
    priority = 4
    category = "Utilities"

    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
        {'name': 'Data', 'type': builtins.object, 'handler': 'set_data', 'flags': 0},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': builtins.object, 'flags': 0},
    ]

    want_main_area = False

    batching = Setting(None)
    batchsize = Setting(None)
    max_input_lag = Setting(None)
    max_output_lag = Setting(None)
    axis = Setting(None)

    def __init__(self):
        super().__init__()

        # Construct node instance and set default properties.
        self.node = BatchPackets()
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('batching', self.node.batching)
            super().__setattr__('batchsize', self.node.batchsize)
            super().__setattr__('max_input_lag', self.node.max_input_lag)
            super().__setattr__('max_output_lag', self.node.max_output_lag)
            super().__setattr__('axis', self.node.axis)
        else:
            self.node.batching = self.batching
            self.node.batchsize = self.batchsize
            self.node.max_input_lag = self.max_input_lag
            self.node.max_output_lag = self.max_output_lag
            self.node.axis = self.axis

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.batching_control = gui.lineEdit(box, self, 'batching', 'Batching:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('batching'), tooltip="Batching mode. If set to 'realtime', then as many packets are merged as necessary to maintain real-time updates. If set to 'fixed', then a fixed number of successive packets (batchsize) are merged.")
        self.batchsize_control = gui.lineEdit(box, self, 'batchsize', 'Batchsize:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('batchsize'), tooltip="Number of successive packets to merge. Only used if batching is set to 'fixed'.")
        self.max_input_lag_control = gui.lineEdit(box, self, 'max_input_lag', 'Max input lag:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_input_lag'), tooltip="Maximum input packet lag beyond which the system will stash the packet and batch it with the next one (in 'realtime' mode), in seconds.")
        self.max_output_lag_control = gui.lineEdit(box, self, 'max_output_lag', 'Max output lag:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('max_output_lag'), tooltip="Maximum delay incurred by batching packets, in seconds.")
        self.axis_control = gui.lineEdit(box, self, 'axis', 'Axis:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('axis'), tooltip="Axis to concatenate along. If set to 'auto', concatenation goes along the instance axis if present, or time axis otherwise.")
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
        node = BatchPackets()

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
    ow = OWBatchPackets()
    ow.show()
    app.exec_()