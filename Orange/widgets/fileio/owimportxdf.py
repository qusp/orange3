# -*- coding: utf-8 -*-

import builtins

from Orange.widgets import widget, gui, cpewidget
from Orange.widgets.settings import Setting
import neuropype.engine
from neuropype.nodes.fileio import ImportXDF


class OWImportXDF(cpewidget.CPEWidget):

    # Node meta-data.
    name = "Import XDF"
    description = "Load data from a .xdf file"
    author = "Christian Kothe"
    icon = "icons/ImportXDF.svg"
    priority = 2
    category = "Fileio"

    # Input/output ports.
    inputs = [
        {'name': 'Update', 'type': builtins.object, 'handler': 'set_update', 'flags': widget.Explicit},
    ]

    outputs = [
        {'name': 'Update', 'type': builtins.object, 'flags': 0},
        {'name': 'This', 'type': builtins.object, 'flags': 0},
        {'name': 'Data', 'type': neuropype.engine.packet.Packet, 'flags': 0},
    ]

    # Configuration properties.
    filename = Setting(None)
    verbose = Setting(None)
    retain_streams = Setting(None)
    handle_clock_sync = Setting(None)
    handle_jitter_removal = Setting(None)
    handle_clock_resets = Setting(None)

    def __init__(self):
        # Initialize with a newly instantiated node.
        super().__init__(ImportXDF())

        # Set default properties.
        settings = self.settingsHandler.pack_data(self)
        if not [k for k, v in settings.items() if v != None]:
            super().__setattr__('filename', self.node.filename)
            super().__setattr__('verbose', self.node.verbose)
            super().__setattr__('retain_streams', self.node.retain_streams)
            super().__setattr__('handle_clock_sync', self.node.handle_clock_sync)
            super().__setattr__('handle_jitter_removal', self.node.handle_jitter_removal)
            super().__setattr__('handle_clock_resets', self.node.handle_clock_resets)
        else:
            self.node.filename = self.filename
            self.node.verbose = self.verbose
            self.node.retain_streams = self.retain_streams
            self.node.handle_clock_sync = self.handle_clock_sync
            self.node.handle_jitter_removal = self.handle_jitter_removal
            self.node.handle_clock_resets = self.handle_clock_resets

        # Initialize GUI controls for editing node properties.
        box = gui.widgetBox(self.controlArea, 'Properties')
        self.filename_control = gui.lineEdit(box, self, 'filename', 'Filename:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('filename'), tooltip="File name to load (*.xdf or *.xdfz).")
        self.verbose_control = gui.checkBox(box, self, 'verbose', 'Verbose', callback=lambda: self.property_changed('verbose'), tooltip="Whether to print diagnostics.")
        self.retain_streams_control = gui.lineEdit(box, self, 'retain_streams', 'Retain streams:', orientation='horizontal', enterPlaceholder=True, callback=lambda: self.property_changed('retain_streams'), tooltip="Streams to retain. The order doesn't actually matter (it's always data streams first, marker streams second).")
        self.handle_clock_sync_control = gui.checkBox(box, self, 'handle_clock_sync', 'Handle clock sync', callback=lambda: self.property_changed('handle_clock_sync'), tooltip="Enable clock synchronization. Needed if data were recorded across multiple computers.")
        self.handle_jitter_removal_control = gui.checkBox(box, self, 'handle_jitter_removal', 'Handle jitter removal', callback=lambda: self.property_changed('handle_jitter_removal'), tooltip="Enable jitter removal for regularlysampled streams.")
        self.handle_clock_resets_control = gui.checkBox(box, self, 'handle_clock_resets', 'Handle clock resets', callback=lambda: self.property_changed('handle_clock_resets'), tooltip="Handle clock resets. Whether the importer should check for potential resets of the clock of a stream (e.g. computer restart during recording, or hot-swap).")
        self.reset_button = gui.button(box, self, 'Reset defaults', autoDefault=False, callback=self.reset_default_properties)

    # Port setters.
    def set_update(self, update):
        self.node.update = update
