"""

"""
import pkg_resources


# Entry point for main Orange categories/widgets discovery
def widget_discovery(discovery):
    #from . import data
    dist = pkg_resources.get_distribution("Orange")
    pkgs = [
         "Orange.widgets.custom",
         "Orange.widgets.elementwise",
         "Orange.widgets.feature_extraction",
         "Orange.widgets.fileio",
         "Orange.widgets.filters",
         "Orange.widgets.formatting",
         "Orange.widgets.general",
         "Orange.widgets.machine_learning",
         "Orange.widgets.network",
         "Orange.widgets.spectral",
         "Orange.widgets.utilities",
         "Orange.widgets.visualization",
         "Orange.widgets.workflow"]
    for pkg in pkgs:
        discovery.process_category_package(pkg, distribution=dist)
