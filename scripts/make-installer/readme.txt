Steps for building a new Windows installer (assuming that you have the CPE and
VPE installed and working):

1. copy contents of this directory into a new folder
2. ensure that that folder does not already contain a previously-created
   installer (if you reuse the folder)
3. copy both cpe/vpe folders to sandbox
4. ensure that the cpe/vpe folders each do not contain a venv or .idea directory
5. copy your venv directory into the target folder and rename it to python
6. copy the following 2 files from C:\Windows\SysWOW64 (or *only* if that doesn't 
   exist, from C:\Windows\system32) to python\Scripts: python34.dll, msvcr100.dll
7. run generate_file_list.py (you should see a files.nsi and unfiles.nsi
   pop up); this requires Python 3.x (best to do that in the console)
8. make sure you have NSIS 3.x installed
9. right-click installer.nsi and select "Compile NSIS Script"
