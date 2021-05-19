from .GING import (
    Sprite,
    KeyCode
)


class Bomberman(Sprite):
    # noinspection PyAttributeOutsideInit
    def start(self):
        self.animator.playing = False
        self.speed = 2

    def update(self):
        if self.input.get_key(KeyCode.Key_W) or self.input.get_key(KeyCode.Key_Up):
            self.animator.playing = True
            self.animator.trigger("back")
            self.transform.position.y += self.speed
        elif self.input.get_key(KeyCode.Key_S) or self.input.get_key(KeyCode.Key_Down):
            self.animator.playing = True
            self.animator.trigger("front")
            self.transform.position.y -= self.speed
        elif self.input.get_key(KeyCode.Key_A) or self.input.get_key(KeyCode.Key_Left):
            self.animator.playing = True
            self.animator.trigger("side")
            self.render.flipX = True
            self.transform.position.x -= self.speed
        elif self.input.get_key(KeyCode.Key_D) or self.input.get_key(KeyCode.Key_Right):
            self.animator.playing = True
            self.animator.trigger("side")
            self.render.flipX = False
            self.transform.position.x += self.speed
        else:
            self.animator.playing = False
        if self.input.get_key(KeyCode.Key_Space):
            bomb = self.game_application.instantiate(
                self.game_application.find("bomb"),
                "bomb_placed"
            )
            if bomb is not None:
                bomb.transform.position.x = self.transform.position.x
                bomb.transform.position.y = self.transform.position.y - 35
                bomb.render.enable = True

    def collision_enter(self, other):
        if other.startswith("flame") or other.startswith("evil"):
            self.game_application.remove(self)
