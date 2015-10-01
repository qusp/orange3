set PYTHONHOME=
set "PATH=%cd%\python\Scripts;%PATH%"
cd vpe
"%cd%\..\python\Scripts\python.exe" setup.py develop
"%cd%\..\python\Scripts\python.exe" setup_qt.py
cd ..

