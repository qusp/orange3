from __future__ import absolute_import
from importlib import import_module

try:
    from .import version
    # Always use short_version here (see PEP 386)
    __version__ = version.short_version
    __git_revision__ = version.git_revision
except ImportError:
    __version__ = "unknown"
    __git_revision__ = "unknown"

ADDONS_ENTRY_POINT = 'orange.addons'

import warnings
import pkg_resources

