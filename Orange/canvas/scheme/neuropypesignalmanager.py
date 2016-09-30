# -*- coding: utf-8 -*-

"""Implements the NeuropypeSignalManager class."""

import logging
import threading

from PyQt4.QtCore import QTimer

from neuropype.engine.graph import Graph
from neuropype.engine.helpers import is_calibrating
from neuropype.engine.scheduler import Scheduler

from .signalmanager import SignalManager


log = logging.getLogger(__name__)


def get_human_readable_state(state):
    if state == SignalManager.Running:
        return 'running'
    if state == SignalManager.Stoped:
        return 'stoped'
    if state == SignalManager.Paused:
        return 'paused'
    if state == SignalManager.Error:
        return 'error'

    raise RuntimeError('Unknown state %r' % state)


class NeuropypeSignalManager(SignalManager):
    """
    A SignalManager implementation that can hold and invoke NeuroPype nodes.
    This class owns a NeuroPype Graph and Scheduler object, and updates both
    in response to GUI actions (add/remove node/link, start/stop/resume).
    """

    def __init__(self, scheme, frequency=25, auto_start=False):
        super().__init__(scheme)
        self._frequency = frequency  # update frequency

        # the neuropype processing graph and scheduler, owned by this object
        self._graph = Graph()
        self._scheduler = Scheduler(self._graph)

        # a mutex to ensure that ticking and structural updates do not
        # collide
        self._mutex = threading.Lock()

        # a timer that allows the scheduler to be updated in the background
        self._timer = None

        # the calibrating state on the last tick (used to emit change events)
        self._was_calibrating = False

        # hook up signal handlers
        def on_state_changed(state):
            log.info('SchedulingManager %r has changed state to %r.',
                self, get_human_readable_state(state).upper())

        def on_scheme_destroyed():
            self.stop()

        self.stateChanged.connect(on_state_changed)
        scheme.destroyed.connect(on_scheme_destroyed)
        scheme.link_added.connect(self.link_added)
        scheme.link_removed.connect(self.link_removed)

        # handle autostart
        if auto_start:
            self.start()

    def link_to_widget_manager(self, widget_manager):
        """Hook up handlers to the widget manager's signals."""
        widget_manager.widget_for_node_added.connect(self.on_node_added)
        widget_manager.widget_for_node_removed.connect(self.on_node_removed)

    # === GETTERS/SETTERS ===

    @property
    def graph(self):
        return self._graph

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency

    # === OVERRIDES ===

    def start(self):
        if self.state() == SignalManager.Stoped:
            self._scheduler.start()
            self._start_timer()
            self.stateChanged.emit(SignalManager.Running)

    def stop(self):
        if self.state() in (SignalManager.Running, SignalManager.Paused):
            self._stop_timer()
            self._scheduler.stop()
            self.stateChanged.emit(SignalManager.Stoped)

    def pause(self):
        if self.state() == SignalManager.Running:
            self._stop_timer()
            self.stateChanged.emit(SignalManager.Paused)

    def resume(self):
        if self.state() == SignalManager.Stoped:
            self.start()
        elif self.state() == SignalManager.Paused:
            self._start_timer()
            self.stateChanged.emit(SignalManager.Running)

    def step(self):
        if self.state() == SignalManager.Paused:
            self._scheduler.advance()

    def state(self):
        if self._scheduler.is_started():
            if self._timer:
                return SignalManager.Running
            else:
                return SignalManager.Paused
        return SignalManager.Stoped

    def on_node_added(self, node, widget):
        try:
            node = widget.node
        except AttributeError:
            return

        self.lock()
        try:
            self._graph.add_node(node)
        finally:
            self.unlock()

        log.info('Added node %r to graph %r.', node, self._graph)

    def on_node_removed(self, node, widget):
        try:
            node = widget.node
        except AttributeError:
            return

        self.lock()
        try:
            self._graph.remove_node(node)
        finally:
            self.unlock()

        log.info('Removed node %r from graph %r.', node, self._graph)

    def link_added(self, link):
        src_node = self._orange_to_pybcilab_node(link.source_node)
        dst_node = self._orange_to_pybcilab_node(link.sink_node)

        if src_node and dst_node:
            src_port = self._channel_to_port_name(src_node, link.source_channel.name)
            dst_port = self._channel_to_port_name(dst_node, link.sink_channel.name)

            if src_port and dst_port:

                self.lock()
                try:
                    self._graph.connect((src_node, src_port), (dst_node, dst_port))
                finally:
                    self.unlock()

                log.info('Added link from (%r, %r) to (%r, %r) in graph %r.',
                    src_node, src_port, dst_node, dst_port, self._graph)

    def link_removed(self, link):
        src_node = self._orange_to_pybcilab_node(link.source_node)
        dst_node = self._orange_to_pybcilab_node(link.sink_node)

        if src_node and dst_node:
            src_port = self._channel_to_port_name(src_node, link.source_channel.name)
            dst_port = self._channel_to_port_name(dst_node, link.sink_channel.name)

            if src_port and dst_port:

                self.lock()
                try:
                    self._graph.disconnect((src_node, src_port), (dst_node, dst_port))
                finally:
                    self.unlock()

                log.info('Removed link from (%r, %r) to (%r, %r) in graph %r.',
                    src_node, src_port, dst_node, dst_port, self._graph)

    def send_to_node(self, node, signals):
        pass

    # === INTERNALS ===

    def _orange_to_pybcilab_node(self, node):
        try:
            return self.scheme().widget_for_node(node).node
        except (AttributeError, KeyError):
            return None

    def _channel_to_port_name(self, node, channel_name):
        for name, port in node.ports().items():
            if port.verbose_name.lower() == channel_name.lower():
                return name
        return None

    def lock(self):
        self._mutex.acquire()

    def unlock(self):
        self._mutex.release()

    def _start_timer(self):
        if not self._timer:
            self._timer = QTimer()
            self._timer.timeout.connect(self._tick)
            self._timer.start(self._frequency)

    def _stop_timer(self):
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _tick(self):
        self.lock()
        try:
            self._scheduler.advance()
            self._emit_calibrating_events()
        finally:
            self.unlock()

    def _emit_calibrating_events(self):
        """Track and emit change events for the "calibrating" state."""
        calibrating = is_calibrating(self._graph)
        if calibrating != self._was_calibrating:
            if calibrating:
                self.calibratingStarted.emit()
            else:
                self.calibratingStopped.emit()
            self._was_calibrating = calibrating
