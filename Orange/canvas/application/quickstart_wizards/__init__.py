import importlib
import inspect
import logging
import os
import pkg_resources
import types

from itertools import chain
from .quickstartwizarddialog import QuickstartWizardDialog


log = logging.getLogger(__name__)


def list_schemes(package):
    resources = pkg_resources.resource_listdir(package.__name__, ".")
    resources = list(filter(is_ows, resources))
    return sorted(resources)


def is_ows(filename):
    return filename.endswith(".ows")


def default_entry_point():
    dist = pkg_resources.get_distribution("Orange")
    ep = pkg_resources.EntryPoint("Orange Canvas", __name__, dist=dist)
    return ep


def quickstart_wizard_entry_points():
    default = default_entry_point()
    return chain([default],
                 pkg_resources.iter_entry_points("orange.widgets.quickstart_wizards"))


def quickstart_wizards():
    all_quickstart_wizards = []
    for ep in quickstart_wizard_entry_points():
        quickstart_wizards = None
        try:
            quickstart_wizards = ep.load()
        except pkg_resources.DistributionNotFound as ex:
            log.warning("Could not load quickstart wizards from %r (%r)",
                        ep.dist, ex)
            continue
        except ImportError:
            log.error("Could not load quickstart wizards from %r",
                      ep.dist, exc_info=True)
            continue
        except Exception:
            log.error("Could not load quickstart wizards from %r",
                      ep.dist, exc_info=True)
            continue

        if isinstance(quickstart_wizards, types.ModuleType):
            package = quickstart_wizards
            quickstart_wizards = list_schemes(quickstart_wizards)
            quickstart_wizards = [QuickstartWizard(w, package, ep.dist) for w in quickstart_wizards]
        elif isinstance(quickstart_wizards, (types.FunctionType, types.MethodType)):
            try:
                quickstart_wizards = quickstart_wizards()
            except Exception as ex:
                log.error("A callable entry point (%r) raised an "
                          "unexpected error.",
                          ex, exc_info=True)
                continue
            quickstart_wizards = [QuickstartWizard(w, package=None, distribution=ep.dist) for w in quickstart_wizards]

        all_quickstart_wizards.extend(quickstart_wizards)

    return all_quickstart_wizards


class QuickstartWizard(object):
    def __init__(self, resource, package=None, distribution=None):
        self.resource = resource
        self.package = package
        self.distribution = distribution
        self.dialog = self.load_dialog()

    def abspath(self):
        if self.package is not None:
            return pkg_resources.resource_filename(self.package.__name__,
                                                   self.resource)
        elif isinstance(self.resource, str):
            if os.path.isabs(self.resource):
                return self.resource

        raise ValueError("cannot resolve resource to an absolute name")

    def stream(self):
        if self.package is not None:
            return pkg_resources.resource_stream(self.package.__name__,
                                                 self.resource)
        elif isinstance(self.resource, str):
            if os.path.isabs(self.resource) and os.path.exists(self.resource):
                return open(self.resource, "rb")

        raise ValueError

    def load_dialog(self):
        resource = self.resource.replace('.ows', '')
        module = importlib.import_module(self.package.__name__ + '.' + resource)

        for key, value in inspect.getmembers(module):
            if isinstance(value, type) and issubclass(value, QuickstartWizardDialog) and value != QuickstartWizardDialog:
                return value

        raise ValueError('Could not load quickstart wizard dialog for %r' % (self.resource,))
