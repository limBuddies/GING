from .GING import (
    Sprite
)


def get_sprite(obj, name) -> Sprite:
    return getattr(obj, name)()
