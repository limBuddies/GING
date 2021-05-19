import time
import random

from .GING import (
    Sprite,
    Vector2
)


# noinspection PyAttributeOutsideInit
class Timer(Sprite):
    def start(self):
        self.start_time = time.time()
        self.last_evil = 0
        self.evil_count = 0
        self.spawns = [
            Vector2(-200, 200),
            Vector2(200, 200),
            Vector2(-200, -200),
            Vector2(200, -200)
        ]

    def update(self):
        if self.game_application.find("bomberman") is not None:
            live_time = round(time.time() - self.start_time)
            self.context = "存活时间：" + str(live_time) + "秒"
            if time.time() - self.last_evil > 5:
                self.last_evil = time.time()
                self.evil_count += 1
                evil = self.game_application.find("evil")
                new_evil = self.game_application.instantiate(evil, "evil" + str(self.evil_count))
                if new_evil is not None:
                    new_evil.transform.position = random.choice(self.spawns)
                    new_evil.render.enable = True
                    new_evil.collision.enable = True
