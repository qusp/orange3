@echo off
echo Launching LabRecorder...
set PYTHONHOME=
set "PATH=%cd%\python;%PATH%"
cd lsl\Apps\LabRecorder\src
python LabRecorder.py