import os
import json


def load(path):
    project_name = os.path.split(path)[1]
    scene = json.loads(open(os.path.join(path, project_name + ".scene")).read())
    print(scene)
