# pkg_resources selects a suitable resource loader based on the modules's
# __loader__ attribute. In python2 it defaults to None, which maps to the
# default resource loader, but it python3 it does not. As a result,
# pkg_resources is unable to select a resource loader and load resources.
# By settings __loader__ to None, we workaround the pkg_resources bug.

# for Python 3.4.4 on Windows this line causes loading the orange.qss file to break...
#__loader__ = None
