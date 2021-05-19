import time

from .GING import (
    Sprite
)


# noinspection PyAttributeOutsideInit
class Flame(Sprite):
    def start(self):
        self.render.enable = False
        self.collision.enable = False
        self.start_time = 0

    def update(self):
        if self.render.enable:
            if self.start_time == 0:
                self.start_time = time.time()
            elif time.time() - self.start_time > 2:
                self.game_application.remove(self)

    def collision_enter(self, other):
        if not other.startswith("flame"):
            self.game_application.remove(self)
