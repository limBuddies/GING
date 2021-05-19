from .Transform import Transform
from .Render import Render
from .Collision import Collision
from .Animator import Animator
from .Vector2 import Vector2


class Sprite:
    def __init__(self):
        self.transform = Transform()
        self.render = Render()
        self.collision = Collision()
        self.animator = Animator()
        self.script_instance = None
        self.context = ""
        self.input = None
        self.sound = None
        self.is_text = False
        self.game_application = None
        self.class_name = ""
        self.lastPositions = Vector2()

    def start(self):
        pass

    def update(self):
        pass
