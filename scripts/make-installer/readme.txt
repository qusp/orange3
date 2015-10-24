Steps for building a new Windows installer (assuming that you have the CPE and
VPE installed and working):

* copy contents of this directory into a new sandbox folder
* ensure that the sandbox does not already contain a previously-created
  installer (if you reuse the folder)
* copy both cpe/vpe folders to the sandbox
* ensure that the cpe/vpe folders each do not contain a venv, .git, or .idea
  directory
* perform the installation procedure for the vpe directory *without* using a
  virtual environment (i.e., against your C:\Python34\ install)
* copy your C:\Python34 directory into the sandbox and rename it to python
* copy the following 2 files from C:\Windows\SysWOW64 (or *only* if that doesn't
  exist, from C:\Windows\system32) to the python folder: python34.dll, msvcr100.dll
* extract the .zip file ftp://sccn.ucsd.edu/pub/software/LSL/Apps/Apps-ALL-1.10.zip
  to lsl/
* extract the .zip file ftp://sccn.ucsd.edu/pub/software/LSL/SDK/liblsl-ALL-languages-1.10.2.zip
  to lsl/; remove the contents of the folder lsl/LSL/liblsl/external/ to reduce
  installer size
* make a folder named docs/ and copy versions of the NeuroPype Manual and
  NeuroPype Release Notes there (not included in this repo)
* run generate_file_list.py (you should see a files.nsi and unfiles.nsi
  pop up); this requires Python 3.x (best to do that in the console)
* make sure you have NSIS 3.x installed
* right-click installer.nsi and select "Compile NSIS Script"


Making a source code release:
* pick all folders, except for python and the license.rtf file
* compress them into a .zip archive
* name the resulting file neuropype-community-src-x.y.z.zip
  (x,y,z being version number parts).

Troubleshooting:
* Why are my svg images not loading after deployment?
  - a file named qt.conf must be generated on the Python search path,
    which must have a [Paths] section that points to the PyQt4 folder after
    installation, using absolute paths and forward slashes even on windows
  - without this file and the correct paths, Qt will not find its own plugins,
    and one of those plugins is the SVG loader
* Why are there files left over after uninstalling NeuroPype?
  - the NSIS installer (and many others) will only remove files that it itself
    created, and so if you are running additional setup scripts that create
    extra files, or if Python creates extra files during launch, the folders
    will not be empty and therefore not be deleted; warning: the correct fix
    is not to delete *.* in the Qusp install folder, because a user may
    (perhaps inadvertently) install NeuroPype to C:\ or the like. instead,
    make sure you delete only the sub-directories and their files that you
    created