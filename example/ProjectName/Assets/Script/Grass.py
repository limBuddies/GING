from .GING import (
    Sprite,
    Vector2,
    KeyCode
)


class Grass(Sprite):
    def start(self):
        # self.transform.position = Vector2(10, 10)
        pass

    def update(self):
        if self.input.get_key(KeyCode.Key_W):
            self.transform.position.y += 1
        if self.input.get_key(KeyCode.Key_S):
            self.transform.position.y -= 1
        if self.input.get_key(KeyCode.Key_A):
            self.transform.position.x -= 1
        if self.input.get_key(KeyCode.Key_D):
            self.transform.position.x += 1
        self.animator.playing = not self.input.get_key(KeyCode.Key_Space)
        if self.input.get_key(KeyCode.Key_Q):
            self.sound.play("bomb_explosion")
        if self.input.get_key(KeyCode.Key_Escape):
            pass
