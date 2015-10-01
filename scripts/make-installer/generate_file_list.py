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
            if outpath != lastpath:
                print('SetOutPath "$INSTDIR\%s"' % outpath, file=out)
                lastpath = outpath
            filename = line[2:]
            if filename not in ['files.nsi','unfiles.nsi',
                                'installer.nsi','generate_file_list.py']:
                print('File "${srcdir}\%s"' % line[2:], file=out)

with open("unfiles.nsi", "w") as out:
    for root, dirs, files in os.walk(".", topdown=False):
        for f in files:
            line = os.path.join(root, f)
            print('Delete "$INSTDIR\%s"' % line[2:], file=out)
        for d in dirs:
            line = os.path.join(root, d)
            print('RMDir "$INSTDIR\%s"' % line[2:], file=out)
