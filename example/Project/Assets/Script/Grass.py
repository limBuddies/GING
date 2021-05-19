from .GING import (
    Sprite,
    KeyCode
)


# noinspection DuplicatedCode
class Grass(Sprite):
    def start(self):
        # self.transform.position = Vector2(10, 10)
        pass

    def collision_enter(self, other):
        print(other)

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
            t1 = self.game_application.instantiate(self.game_application.find("New Text"), "New Text1")
            if t1 is not None:
                t1.transform.position.x -= 20
                t1.transform.position.y -= 20
        if self.input.get_key(KeyCode.Key_Escape):
            self.game_application.close()
        if self.input.get_key(KeyCode.Key_E):
            self.animator.trigger("T1")
            print(self.game_application.find("grass").transform.position.y)
            print(self.game_application.find_by_class("Grass"))
