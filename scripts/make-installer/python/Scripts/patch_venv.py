import os
with open("activate.bat.template","r") as f:
    content = f.read()

this_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
content = content.replace("$(INSTALLPATH)", this_path)

with open("activate.bat","w") as f:
    f.write(content)
