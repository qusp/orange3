Steps for building a new Windows installer (assuming that you have the CPE and
VPE installed and working):

1. copy contents of this directory into a new sandbox folder
2. ensure that the sandbox does not already contain a previously-created
   installer (if you reuse the folder)
3. copy both cpe/vpe folders to the sandbox
4. ensure that the cpe/vpe folders each do not contain a venv or .idea directory
5. perform the installation procedure for the vpe directory *without* using a
   virtual environment (i.e., against your C:\Python34\ install)
6. copy your C:\Python34 directory into the sandbox and rename it to python
7. copy the following 2 files from C:\Windows\SysWOW64 (or *only* if that doesn't 
   exist, from C:\Windows\system32) to the python folder: python34.dll, msvcr100.dll
8. run generate_file_list.py (you should see a files.nsi and unfiles.nsi
   pop up); this requires Python 3.x (best to do that in the console)
9. make sure you have NSIS 3.x installed
10. right-click installer.nsi and select "Compile NSIS Script"
