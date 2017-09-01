"""Regenerate the widget tree from a given NeuroPype installation.

Note that this script must be run in a Python environment that can import the
neuropype package and some of its sub-packages (from the given path, if
overridden).

By default the script will use the neuropype installation on the Python path,
and will modify the Orange installation that contains this script.

Copyright (C) 2014-2016 Syntrogi Inc (dba Qusp). All rights reserved.
"""

import argparse
import os
import sys
import re
import shutil
import importlib
import inspect

import jinja2

# these are reserved packages in the Orange/widgets folder that are not usable
# as neuropype module names
reserved_widget_packages = {'utils', 'icons'}

# background colors that will be used for the widget categories (in that order,
# and wrapping around if there are more categories than colors)
widget_colors = ["#FFD39F", "#FFA840", "#FFB7B1", "#FAC1D9", "#E5BBFB",
                 "#CAE1FC", "#C3F3F3", "#ACE3CE", "#DFECB0", "#F7F5A7"]

# list of destination paths at which to place icons
# (icons are sourced from a common 'icons' directory)
icons_needed = []


def snake2camel(s, with_spaces=False):
    """Convert snake_case to CamelCase (or Camel Case)."""
    sep = ' ' if with_spaces else ''
    return sep.join(word.capitalize() for word in s.split('_'))


def sanitize_neuropype_path(neuropype_path):
    """Resolve the path to neuropype if necessary and ensure that we can import
    from that path."""
    if not neuropype_path:
        import neuropype
        neuropype_path = os.path.dirname(neuropype.__file__)
    else:
        sys.path.insert(0, os.path.dirname(neuropype_path))
        import neuropype
        if neuropype_path != os.path.dirname(neuropype.__file__):
            print("Could not import neuropype from given path: %s" %
                  neuropype_path)
            sys.exit(1)

    if not os.path.exists(neuropype_path):
        print("Error: path does not exist: %s" % neuropype_path)
        sys.exit(1)
    else:
        print("Assuming NeuroPype path: %s" % neuropype_path)

    return neuropype_path


def sanitize_orange_path(orange_path):
    """Resolve the path to Orange if necessary."""
    if not orange_path:
        script_dir = os.path.dirname(__file__)
        orange_path = os.path.normpath(os.path.join(script_dir, '..', 'Orange'))

    if not os.path.exists(orange_path):
        print("Error: path does not exist: %s" % orange_path)
        sys.exit(1)
    else:
        print("Assuming Orange path: %s" % orange_path)

    return orange_path


def sanitize_resource_path(resource_path):
    """Resolve the path where resource files live if necessary."""
    if not resource_path:
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, 'widget-resources')

    if not os.path.exists(resource_path):
        print("Error: path does not exist: %s" % resource_path)
        sys.exit(1)
    else:
        print("Assuming resource path: %s" % resource_path)

    return resource_path


def find_modules(path_to_neuropype):
    """Get the list of module names from the neuropype path."""
    # get the path to the node packages
    node_path = os.path.join(path_to_neuropype, 'nodes')

    # find all module names
    modules = [f[:-3] for f in os.listdir(node_path)
               if f.endswith('.py') and f != '__init__.py']
    modules.sort()
    print("Found neuropype modules: %s" % modules)

    # ensure that there are no directory name clashes
    invalid = set(modules) & reserved_widget_packages
    if invalid:
        print("Error: some neuropype modules clash with reserved Orange "
              "packages: %s" % invalid)
        sys.exit(1)

    return modules


def update_setup_py(filename, modules):
    """Update the setup.py file in an Orange installation."""

    print("updating setup.py...", end='')

    flags = re.DOTALL | re.MULTILINE

    # first get all the content
    with open(filename, 'r') as f:
        content = f.read()

    # additional packages clause to insert into file
    new_pkgs = ',\n'.join(['    "Orange.widgets.%s"' % m for m in modules])
    new_pkgs_decl = 'PACKAGES += [\n%s\n]\n' % new_pkgs

    # find the PACKAGE = [...] declaration
    pkgs_patt = re.compile(r"^PACKAGES = \[.*?\]$", flags)
    pkgs_decl = pkgs_patt.search(content).span()

    # find the PACKAGES += [...] declaration
    pkgs_ext_patt = re.compile(r"^PACKAGES \+= \[.*?\]$", flags)
    pkgs_ext_decl = pkgs_ext_patt.search(content)

    if not pkgs_ext_decl:
        # if not present, place it after the packages decl
        content = content[:pkgs_decl[1]] + '\n\n' + content[pkgs_decl[1]:]
        pkgs_ext_decl = [pkgs_decl[1]+2, pkgs_decl[1]+2]
    else:
        pkgs_ext_decl = pkgs_ext_decl.span()

    # insert the new modules in place of the packages extension decl
    content = (content[:pkgs_ext_decl[0]] + new_pkgs_decl +
               content[pkgs_ext_decl[1]+1:])

    # additional package data clause to insert into file
    new_pkgdata = ',\n'.join(['    "Orange.widgets.%s": ["icons/*.svg"]' %
                              m for m in modules])
    new_pkgdata_decl = 'PACKAGE_DATA.update({\n%s\n})\n' % new_pkgdata

    # find the PACKAGE_DATA = {...} declaration
    pkgdata_patt = re.compile(r"^PACKAGE_DATA = \{.*?\}$", flags)
    pkgdata_decl = pkgdata_patt.search(content).span()

    # find the PACKAGE_DATA.update({...}) declaration
    pkgdata_ext_patt = re.compile(r"^PACKAGE_DATA\.update\(\{.*?\}\)$", flags)
    pkgdata_ext_decl = pkgdata_ext_patt.search(content)

    if not pkgdata_ext_decl:
        # if not present, place it after the packages decl
        content = content[:pkgdata_decl[1]] + '\n\n' + content[pkgdata_decl[1]:]
        pkgdata_ext_decl = [pkgdata_decl[1]+2, pkgdata_decl[1]+2]
    else:
        pkgdata_ext_decl = pkgdata_ext_decl.span()

    # insert the new modules in place of the packages extension decl
    content = (content[:pkgdata_ext_decl[0]] + new_pkgdata_decl +
               content[pkgdata_ext_decl[1]+1:])
    # now write the new content to the file
    with open(filename, 'w') as f:
        f.write(content)

    print("done.")


def update_widget_registration(filename, modules):
    """Updates the widgets/__init__.py file in an Orange installation."""

    print("updating widget registration...", end='')

    # first get all the content
    with open(filename, 'r') as f:
        content = f.read()

    # find the pkgs = [...] declaration
    pkgs_patt = re.compile(r"pkgs = \[.*?\]", re.DOTALL | re.MULTILINE)
    pkgs_decl = pkgs_patt.search(content).span()

    # replace by a new declaration
    new_pkgs = ',\n'.join(['         "Orange.widgets.%s"' % m for m in modules])
    new_pkgs_decl = 'pkgs = [\n%s]' % new_pkgs
    content = (content[:pkgs_decl[0]] + new_pkgs_decl +
               content[pkgs_decl[1]:])

    # rewrite file
    with open(filename, 'w') as f:
        f.write(content)

    print("done.")


def recreate_widget_directories(widget_path, modules):
    """Ensures that for each module there is an empty directory in the widgets
    path; removes any unlisted and unreserved directories."""

    print("removing old widget directories...", end='')

    # remove old directories
    candidates = set(os.listdir(widget_path)) - reserved_widget_packages
    for d in candidates:
        candidate = os.path.join(widget_path, d)
        if os.path.isdir(candidate):
            shutil.rmtree(candidate)

    print("done.\ncreating new widget directories...", end='')

    # create new directories
    for m in modules:
        os.mkdir(os.path.join(widget_path, m))
        os.mkdir(os.path.join(widget_path, m, 'icons'))

    print("done.")


def create_widget_init_files(widget_path, modules):
    """Create __init__.py files for the widget packages."""

    print("creating new widget __init__.py files...", end='')

    for k, m in enumerate(modules):
        init_path = os.path.join(widget_path, m, '__init__.py')
        with open(init_path, 'w') as f:
            print("NAME = '%s'" % snake2camel(m, with_spaces=True), file=f)
            print("ID = 'orange.widgets.%s'" % m, file=f)
            try:
                node = importlib.import_module('neuropype.nodes.%s' % m)
                desc = node.__doc__.split('\n')[0]
            except ImportError as e:
                print("  could not import neuropype.nodes.%s; leaving package "
                      "description unassigned (%s)." % (m, e))
                desc = '(no description)'
            print("DESCRIPTION = '%s'" % desc, file=f)
            icon_path = "icons/Category-%s.svg" % snake2camel(m)
            print("ICON = '%s'" % icon_path, file=f)
            icon_path_full = os.path.join(widget_path, m, icon_path)
            icons_needed.append(icon_path_full)
            print("BACKGROUND = '%s'" % widget_colors[k % len(widget_colors)],
                  file=f)
            print("PRIORITY = %i" % (k+1), file=f)

    print("done.")


def generate_widget_code(resource_path, widget_path, modules):
    """Generate widget wrapper code for each node in neuropype."""
    from neuropype.engine.node import Node
    print("generating widget code...", end='')

    # try to load code generation template...
    loader = jinja2.FileSystemLoader(resource_path)
    env = jinja2.Environment(loader=loader)
    template = env.get_template('widget.template')

    for modname in modules:

        # gather list of nodes
        nodes = []
        try:
            module = importlib.import_module('neuropype.nodes.%s' % modname)
            for key, value in inspect.getmembers(module):
                if (isinstance(value, type) and issubclass(value, Node)
                        and (not inspect.isabstract(value)) and value != Node):
                    nodes.append(value)
        except ImportError as e:
            print("  could not import module neuropype.nodes.%s; ignoring "
                  "contained nodes (%s)." % (modname, e))

        nodes.sort(key=lambda n: n.__name__)
        for k, node in enumerate(nodes):

            # generate code from template
            content = template.render(node=node, category=modname, priority=k+1,
                                      icon='icons/%s.svg' % node.__name__)

            # write to disk
            out_path = os.path.join(widget_path, modname, 'ow%s.py' %
                                    node.__name__.lower())
            with open(out_path, 'wb') as f:
                f.write(content.encode('utf-8'))

            # also register needed icons
            icon_path = os.path.join(widget_path, modname, 'icons',
                                     node.__name__ + '.svg')
            icons_needed.append(icon_path)

    print("done.")


def copy_icons(source_folder, dest_paths):
    """Copy icons from the source folder to the given destination paths."""
    default_icon = 'Default.svg'

    print("copying icon files...", end='')

    for dest_path in dest_paths:
        name = os.path.basename(dest_path)
        source_path = os.path.join(source_folder, name)
        # fall back to default icon if necessary
        if not os.path.exists(source_path):
            source_path = os.path.join(source_folder, default_icon)
            print("No icon named '%s' found; using default icon." % name)
        try:
            shutil.copyfile(source_path, dest_path)
        except RuntimeError as e:
            print("  could not copy icon file %s (%s)" % (name, e))

    print("done.")


def regenerate_widgets(neuropype_path=None, orange_path=None,
                       resource_path=None):
    """List nodes in a given source neuropype installation and generate a widget
    hierarchy in a target Orange installation.
    """

    # check/set the paths first
    neuropype_path = sanitize_neuropype_path(neuropype_path)
    orange_path = sanitize_orange_path(orange_path)
    resource_path = sanitize_resource_path(resource_path)

    # find module list
    modules = find_modules(neuropype_path)

    # process setup.py
    setup_path = os.path.normpath(os.path.join(orange_path, '..', 'setup.py'))
    update_setup_py(setup_path, modules)

    # process widget/__init__.py
    init_path = os.path.join(orange_path, 'widgets', '__init__.py')
    update_widget_registration(init_path, modules)

    # create and empty widget directories
    widget_path = os.path.join(orange_path, 'widgets')
    recreate_widget_directories(widget_path, modules)

    # create the __init__.py file for the new widget packages
    create_widget_init_files(widget_path, modules)

    # generate widget wrapper code for each node
    generate_widget_code(resource_path, widget_path, modules)

    # copy over the icon files
    icon_path = os.path.join(resource_path, 'icons')
    copy_icons(icon_path, icons_needed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto-generate VPE widgets for'
                                                 ' a NeuroPype installation.')
    parser.add_argument('-n', '--neuropype-path',
                        help='Path to neuropype package for whose nodes to '
                             'generate widgets (default: according to Python '
                             'path).')
    parser.add_argument('-o', '--orange-path',
                        help='Path to Orange package in which to place '
                             'generated widgets (default: relative to this '
                             'file).')
    parser.add_argument('-r', '--resource-path',
                        help='Path to resource files used for widget generation'
                             ' (default: folder named widget-resources relative'
                             ' to this file).')
    args = parser.parse_args()

    regenerate_widgets(args.neuropype_path, args.orange_path,
                       args.resource_path)
