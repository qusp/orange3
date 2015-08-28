"""Regenerate the widget tree from a given NeuroPyPE installation."""

import argparse
import os
import sys
import re
import shutil

# these are reserved packages in the Orange/widgets folder that are not usable
# as neuropype module names
reserved_widget_packages = {'utils', 'icons'}

def update_setup_py(filename, modules):
    """Update the setup.py file in an Orange installation."""

    print("updating setup.py...", end='')

    flags = re.DOTALL | re.MULTILINE

    # first get all the content
    with open(filename, 'r') as f:
        content = f.read()

    # additional packages clause to insert into file
    new_packages = ',\n'.join(['    "Orange.widgets.%s"' % m for m in modules])
    new_packages_decl = 'PACKAGES += [\n%s\n]\n' % new_packages

    # find the PACKAGE = [...] declaration
    packages_patt = re.compile(r"^PACKAGES = \[.*?\]$", flags)
    packages_decl = packages_patt.search(content).span()

    # find the PACKAGES += [...] declaration
    packages_ext_patt = re.compile(r"^PACKAGES \+= \[.*?\]$", flags)
    packages_ext_decl = packages_ext_patt.search(content).span()

    if not packages_ext_decl:
        # if not present, place it after the packages decl
        packages_ext_decl = [packages_decl[1], packages_decl[1]]

    # insert the new modules in place of the packages extension decl
    content[packages_ext_decl[0]:packages_ext_decl[1]] = new_packages_decl

    # additional package data clause to insert into file
    new_packagedata = ',\n'.join(['    "Orange.widgets.%s": ["icons/*.svg"]' % m for m in modules])
    new_packagedata_decl = 'PACKAGE_DATA.update({\n%s\n})\n' % new_packagedata

    # find the PACKAGE_DATA = {...} declaration
    packagedata_patt = re.compile(r"^PACKAGE_DATA = \{.*?\}$", flags)
    packagedata_decl = packagedata_patt.search(content).span()

    # find the PACKAGE_DATA.update({...}) declaration
    packagedata_ext_patt = re.compile(r"^PACKAGE_DATA\.update\(\{.*?\}\)$", flags)
    packagedata_ext_decl = packagedata_ext_patt.search(content).span()

    if not packagedata_ext_decl:
        # if not present, place it after the packages decl
        packagedata_ext_decl = [packagedata_decl[1], packagedata_decl[1]]

    # insert the new modules in place of the packages extension decl
    content[packagedata_ext_decl[0]:packagedata_ext_decl[1]] = new_packagedata_decl

    # now write the new content to the file
    with open(filename, 'w') as f:
        f.write(content)

    print('done.')


def recreate_widget_directories(widget_path, modules):
    """Ensures that for each module there is an empty directory in the widgets
    path; removes any unlisted and unreserved directories."""

    # remove old directories
    to_remove = set(os.listdir(widget_path)) - reserved_widget_packages
    for d in to_remove:
        candidate = os.path.join(widget_path, d)
        if os.path.isdir(candidate):
            shutil.rmtree(candidate)

    # create new directories
    for d in modules:
        os.mkdir(os.path.join(widget_path, d))
        os.mkdir(os.path.join(widget_path, d, 'icons'))


def regenerate_widgets(path_to_neuropype=None, path_to_orange=None):
    """List nodes in a given source neuropype installation and generate a widget
    hierarchy in a target Orange installation.
    """
    # resolve the path to neuropype if necessary (to the current neuropype package)
    if not path_to_neuropype:
        import neuropype
        path_to_neuropype = os.path.dirname(neuropype.__file__)

    if not os.path.exists(path_to_neuropype):
        print("Error: path does not exist: %s" % path_to_neuropype)
        sys.exit(1)

    # resolve the path to Orange if necessary (relative to this script)
    if not path_to_orange:
        path_to_orange = os.path.join(__file__, '..', 'Orange')

    if not os.path.exists(path_to_orange):
        print("Error: path does not exist: %s" % path_to_orange)
        sys.exit(1)

    # get the path to the node packages
    node_path = os.path.join(path_to_neuropype, 'nodes')

    # find all module names
    modules = [f[:-3] for f in os.listdir(node_path)
               if f.endswith('.py') and f != '__init__.py']
    print("Found neuropype modules: %s" % modules)

    # ensure that there are no directory name clashes
    invalid = set(modules) & reserved_widget_packages
    if invalid:
        print("Error: some neuropype modules clash with reserved Orange "
              "packages: %s" % invalid)
        return(1)

    # process setup.py
    setup_path = os.path.join(path_to_orange, '..', 'setup.py')
    update_setup_py(setup_path, modules)

    # create and empty widget directories
    widget_path = os.path.join(path_to_orange, 'widgets')
    recreate_widget_directories(widget_path, modules)


if __name__ == '__main__':
    # parse commandline arguments
    parser = argparse.ArgumentParser(description='Auto-generate VPE widgets for'
                                                 ' a NeuroPyPE installation.')
    parser.add_argument('-n', '--neuropype-path',
                        help='Path to neuropype package for whose nodes to '
                             'generate widgets.')
    parser.add_argument('-o', '--orange-path',
                        help='Path to Orange package in which to place '
                             'generated widgets.')
    args = parser.parse_args()
    regenerate_widgets(args.neuropype_path, args.orange_path)
