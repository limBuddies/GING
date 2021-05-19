import os
from Runtime import *
import Assets.Script
import sys
import json
import subprocess
import shutil

if __name__ == '__main__':
    project_path = os.path.split(os.path.realpath(__file__))[0]
    if len(sys.argv) == 3 and sys.argv[1] == "build":
        os.chdir(project_path)
        if not os.path.exists("Build"):
            os.mkdir("Build")
        if os.path.exists("Build/Assets"):
            shutil.rmtree("Build/Assets")
        if os.path.exists("Build/Runtime"):
            shutil.rmtree("Build/Runtime")
        shutil.copytree(
            os.path.join(project_path, "Assets"),
            "Build/Assets"
        )
        shutil.copytree(
            os.path.join(project_path, "Runtime"),
            "Build/Runtime"
        )
        pack_python = f"data='{json.dumps(Pack.pack(project_path))}'"
        pack_python += """
from Runtime import Entry
import Assets.Script
import json
Entry.enter(json.loads(data), Assets.Script)
"""
        project_name = os.path.split(project_path)[1]
        open(os.path.join(project_path, "Build/" + project_name + ".py"), "w+").write(pack_python)
        os.chdir("Build")
        if sys.argv[2] == "dir":
            subprocess.run("pyinstaller -D --noconsole " + project_name + ".py")
        elif sys.argv[2] == "exe":
            subprocess.run("pyinstaller -F --noconsole " + project_name + ".py")
        for item in os.listdir(os.curdir):
            if os.path.isfile(item):
                os.remove(os.path.join(item))
            else:
                if item != "dist":
                    shutil.rmtree(item)
    else:
        Entry.enter(Pack.pack(project_path), Assets.Script)
