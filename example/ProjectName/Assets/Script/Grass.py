from .GING import (
    Sprite,
    Vector2
)


class Grass(Sprite):
    def start(self):
        self.transform.position = Vector2(10, 10)

    def update(self):
        self.transform.position = Vector2(10, 10)
        print("Grass update")
