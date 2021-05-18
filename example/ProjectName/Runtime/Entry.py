from .GING import (
    Vector2,
    Transform,
    Sprite
)
from . import (
    Misc,
    Window
)


def initialize_sprites(data, script):
    sprites = {}
    for k in data["sprites"].keys():
        sprite = data["sprites"][k]
        if sprite["script"]["class_name"] != "":
            sprite_instance = Misc.get_sprite(script, sprite["script"]["class_name"])
        else:
            sprite_instance = Sprite()
        sprite_position = sprite["transform"]["position"]
        sprite_instance.transform.position = Vector2(sprite_position["x"], sprite_position["y"])
        sprite_instance.render.enable = sprite["render"]["enable"]
        sprite_instance.render.layer = sprite["render"]["layer"]
        sprite_instance.render.scale = sprite["render"]["render_scale"]
        if not sprite["is_text"]:
            sprite_instance.render.flipX = sprite["render"]["flipX"]
            sprite_instance.render.default_frame = sprite["render"]["default_frame"]
            sprite_instance.collision.enable = sprite["collision"]["enable"]
            sprite_instance.collision.size.x = sprite["collision"]["x_size"]
            sprite_instance.collision.size.y = sprite["collision"]["y_size"]
        # Animator 初始化
        sprite_instance.script_instance = sprite_instance
        sprites[k] = sprite_instance
    return sprites


def enter(data, script):
    # grass = Misc.get_sprite(script, "Grass")
    # x = grass.transform
    # y = Vector2(1, 2)
    # x.position = y
    Window.launch()
    initialize_sprites(data, script)
