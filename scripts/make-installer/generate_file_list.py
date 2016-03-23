#!/usr/bin/python

import os


# generate file list

with open("files.nsi", "w") as out:
    for root, dirs, files in os.walk("."):
        if '.git' in root:
            continue
        lastpath = None
        for f in files:
            line = os.path.join(root, f)
            outpath = root[2:]
            if ('.idea' in outpath) or ('venv' in outpath):
                continue
            if outpath != lastpath:
                print('SetOutPath "$INSTDIR\%s"' % outpath, file=out)
                lastpath = outpath
            filename = line[2:]
            if filename in ['files.nsi', 'unfiles.nsi', 'readme.txt',
                            'installer.nsi', 'installer64.nsi',
                            'generate_file_list.py']:
                continue
            if filename.startswith('neuropype') and filename.endswith('.exe'):
                continue
            print('File "${srcdir}\%s"' % line[2:], file=out)

with open("unfiles.nsi", "w") as out:
    for root, dirs, files in os.walk(".", topdown=False):
        for f in files:
            line = os.path.join(root, f)
            print('Delete "$INSTDIR\%s"' % line[2:], file=out)
        for d in dirs:
            line = os.path.join(root, d)
            print('RMDir "$INSTDIR\%s"' % line[2:], file=out)
