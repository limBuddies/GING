from .GING import (
    Vector2,
    Transform,
    Sprite
)
from . import Misc


def enter(data, script):
    grass = Misc.get_sprite(script, "Grass")
    x = grass.transform
    y = Vector2(1, 2)
    x.position = y
