import numpy as np

from Orange.widgets import widget
from neuropype.engine.common import warn_once
from neuropype.engine.ports import ListPort, IntPort

NoneUIValue = ['(use default)', '(default)']


class CPEWidget(widget.OWWidget):

    want_main_area = False

    def __init__(self, node):
        super().__init__()

        # the underlying CPE node instance (wrapped by the widget)
        self.node = node

        # Name of the last node property to generate an error.
        self.last_error_caused_by = ''

        # Set minimum width (in pixels).
        self.setMinimumWidth(360)

    def sync_properties(self):
        """Synchronize our own properties with the defaults of the node at
        creation time."""
        # apply any loaded settings of this widget to the cpe node
        settings = self.settingsHandler.pack_data(self)
        for k, v in settings.items():
            if v is not None:
                setattr(self.node, k, getattr(self, k))

        # apply all defaults from the cpe node that aren't in the settings
        # to the widget
        for n, p in self.node.ports(direction='IN*', editable=True).items():
            if n not in settings or settings[n] is None:
                value = getattr(self.node, n)
                if (isinstance(p, ListPort) or isinstance(p, IntPort)) and value is None:
                    super().__setattr__(n, NoneUIValue[0])
                else:
                    super().__setattr__(n, value)

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
        node = self.node.__class__()

        for name in (names or self.get_property_names()):
            setattr(self.node, name, getattr(node, name))
            value = getattr(self.node, name)
            # Synchronize property changes back to the GUI.
            if (isinstance(self.node.port(name), ListPort)
                or isinstance(self.node.port(name), IntPort))\
                    and value is None:
                value = NoneUIValue[0]
            super().__setattr__(name, value)

    def property_changed(self, name):
        if self.last_error_caused_by and self.last_error_caused_by != name:
            return

        try:
            setNoneUIValue = False
            value_type = self.node.port(name).value_type
            if value_type in (bool, str):
                value = getattr(self, name)
            elif value_type in (list, tuple, set):
                openchars, closechars = "[{(", "])}"
                if value_type == list:
                    openchar, closechar = "[", "]"
                elif value_type == tuple:
                    openchar, closechar = "(", ")"
                else:
                    openchar, closechar = "{", "}"
                content = getattr(self, name)
                # parse list default value and return
                if content in NoneUIValue:
                    content = 'None'
                    setNoneUIValue = True
                else:
                    # handle empty entry
                    if not content:
                        content = "[]"
                    # handle missing brackets
                    if content[0] not in openchars:
                        content = "[" + content
                    if content[-1] not in closechars:
                        content = content + "]"
                    # strip whitespace between brackets and list
                    content = content[0] + content[1:-1].strip() + content[-1]
                    # replace semicolons by commas and warn
                    if ";" in content:
                        content.replace(";", ",")
                        warn_once("Semicolons are not a valid character in "
                                  "NeuroPype lists (replacing by commas).")
                    # handle missing commas in MATLAB-style list literals
                    if " " in content:
                        if "'" in content:
                            pass  # assume that these are quoted strings, ignore
                        elif "," not in content:
                            content = ", ".join(content.split())
                    # fix up specific bracket type
                    if content[0] in openchars and (content[0] != openchar):
                        content = openchar + content[1:]
                    if content[-1] in closechars and (content[-1] != closechar):
                        content = content[:-1] + closechar
                try:
                    # attempt to evaluate as expression
                    value = eval(content, None, np.__dict__)
                except Exception:
                    raise RuntimeError("Incorrectly formatted list: use [value, value, ...] as format.")
            else:
                # Evaluate string as pure Python code.
                content = getattr(self, name)
                try:
                    if content in NoneUIValue:
                        content = 'None'
                        setNoneUIValue = True
                    # attempt to evaluate as expression
                    value = eval(content, None, np.__dict__)
                    if callable(value):
                        # a function is almost certainly not what we wanted
                        raise ValueError("not applicable")
                except Exception as e:
                    # interpret as a string
                    value = eval('"%s"' % content)

            setattr(self.node, name, value)
            # Synchronize property changes back to the GUI.
            if setNoneUIValue:
                super().__setattr__(name, NoneUIValue[0])
            else:
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
