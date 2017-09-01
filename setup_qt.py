import os
import sys
import platform

python_dir = os.path.dirname(os.path.abspath(sys.executable))
print("The Python executable is in: %s" % python_dir)
site_dir = os.path.join(python_dir, "lib", "site-packages")
qt_path = os.path.join(site_dir, "PyQt4").replace("\\", "/")
print("The Qt path is: %s" % qt_path)
with open(os.path.join(python_dir, "qt.conf"), "w") as f:
    print("[Paths]", file=f)
    print("Prefix = %s" % qt_path, file=f)
    print("Binaries = %s" % qt_path, file=f)
