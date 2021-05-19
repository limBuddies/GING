import time
import math

from .GING import (
    Sprite
)


# noinspection PyAttributeOutsideInit
class Bomb(Sprite):
    def start(self):
        self.render.enable = False
        self.start_time = 0

    # noinspection DuplicatedCode
    def update(self):
        if self.render.enable:
            if self.start_time == 0:
                self.start_time = time.time()
            elif time.time() - self.start_time < 3.5:
                scale = math.sin((time.time() - self.start_time) * 5) * 0.3 + 0.7
                self.render.scale = scale
            else:
                self.sound.play("explosion")
                flame = self.game_application.find("flame")
                id_start = int(time.time()) % 12345
                for x in range(5):
                    f = self.game_application.instantiate(flame, "flame" + str(id_start))
                    id_start += 1
                    if f is not None:
                        f.transform.position.x = (x - 2.5) * 50 + self.transform.position.x
                        f.transform.position.y = self.transform.position.y
                        f.render.enable = True
                        f.collision.enable = True
                for y in range(5):
                    f = self.game_application.instantiate(flame, "flame" + str(id_start))
                    id_start += 1
                    if f is not None:
                        f.transform.position.y = (y - 2.5) * 50 + self.transform.position.y
                        f.transform.position.x = self.transform.position.x
                        f.render.enable = True
                        f.collision.enable = True
                self.game_application.remove(self)
