import os
import json
import base64


def pack(path):
    project_name = os.path.split(path)[1]
    scene = json.loads(open(os.path.join(path, project_name + ".scene")).read())
    for k in scene["sprites"].keys():
        sprite = scene["sprites"][k]
        if not sprite["is_text"]:
            sprite_object = json.loads(open(sprite["path"]).read())
            image_path = os.path.join(os.path.split(sprite["path"])[0], sprite_object["image"]["path"])
            image_data = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
            del sprite_object["image"]["path"]
            sprite_object["image"]["data"] = image_data
            del sprite["path"]
            sprite["sprite"] = sprite_object
    for k in scene["sounds"].keys():
        sound_data = base64.b64encode(open(os.path.join(path, scene["sounds"][k]), "rb").read()).decode("utf-8")
        scene["sounds"][k] = sound_data
    return scene
