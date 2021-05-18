from .Transform import Transform
from .Render import Render
from .Collision import Collision
from .Animator import Animator


class Sprite:
    def __init__(self):
        self.transform = Transform()
        self.render = Render()
        self.collision = Collision()
        self.animator = Animator()
        self.script_instance = None

    def start(self):
        pass

    def update(self):
        pass
