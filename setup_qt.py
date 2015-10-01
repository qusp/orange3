import os
import sys

python_dir = os.path.dirname(os.path.abspath(sys.executable))
site_dir = os.path.join(os.path.dirname(python_dir), "lib", "site-packages")
qt_path = os.path.join(site_dir, "PyQt4").replace("\\","/")
with open(os.path.join(python_dir,"qt.conf"),"w") as f:
    print("[Paths]", file=f)
    print("Prefix = %s" % qt_path, file=f)
    print("Binaries = %s" % qt_path, file=f)
