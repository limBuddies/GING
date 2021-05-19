import random

from .GING import (
    Sprite
)


# noinspection PyAttributeOutsideInit
class Evil(Sprite):
    def start(self):
        self.render.enable = False
        self.collision.enable = False
        self.speed = 0.5

    def update(self):
        if self.render.enable:
            bomberman = self.game_application.find("bomberman")
            if bomberman is not None:
                x_delta = self.speed if bomberman.transform.position.x > self.transform.position.x else -self.speed
                y_delta = self.speed if bomberman.transform.position.y > self.transform.position.y else -self.speed
                if self.collision.enable:
                    self.transform.position.x += x_delta
                    self.transform.position.y += y_delta
                else:
                    rand = random.Random()
                    self.transform.position.x += rand.randrange(-2, 2)
                    self.transform.position.y += rand.randrange(-2, 2)

    def collision_enter(self, other):
        if other.startswith("flame"):
            self.game_application.remove(self)
        if other.startswith("evil"):
            self.collision.enable = False

    def collision_exit(self, other):
        if other.startswith("evil"):
            self.collision.enable = True

    def collision_stay(self, other):
        if not other.startswith("evil"):
            rand = random.Random()
            self.transform.position.x += rand.randrange(-2, 2)
            self.transform.position.y += rand.randrange(-2, 2)
