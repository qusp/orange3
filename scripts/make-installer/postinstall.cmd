set PYTHONHOME=
set "PATH=%cd%\python\Scripts;%PATH%"
cd vpe
"%cd%\..\python\python.exe" setup.py develop
"%cd%\..\python\python.exe" setup_qt.py
cd ..

