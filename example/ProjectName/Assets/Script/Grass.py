from .GING import (
    Sprite,
    Vector2,
    KeyCode
)


class Grass(Sprite):
    def start(self):
        self.transform.position = Vector2(10, 10)

    def update(self):
        if self.input.get_key(KeyCode.Key_W):
            self.transform.position.x += 1
        elif self.input.get_key(KeyCode.Key_S):
            self.transform.position.x -= 1
        print(self.transform.position.x)
