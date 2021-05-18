from .gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)
from PyQt5.QtGui import (
    QPixmap,
    QKeyEvent,
    QMouseEvent,
    QPaintEvent,
    QPainter,
    QFont
)
from PyQt5.QtCore import (
    QRect,
    QCoreApplication,
    Qt
)
from .GING import (
    Vector2,
    Sprite
)
from . import (
    Misc,
    InputManager,
    SoundManager
)
import base64
import threading
import time
import copy


class GameWindow(QMainWindow, window.Ui_MainWindow):
    def __init__(self, data, script, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.data = data
        self.script_module = script
        self.input = InputManager.InputManager()
        self.sound = SoundManager.SoundManager(self.data["sounds"])
        self._painter = QPainter()
        self._sprites = self.initialize_sprites()
        self._new_sprites = []
        for k in self._sprites.keys():
            self._sprites[k].start()
        threading.Thread(target=self.ticker).start()

    def ticker(self):
        last_frame = time.time()
        while True:
            if len(self._new_sprites) > 0:
                for s in self._new_sprites:
                    self._sprites[s[0]] = s[1]
            for k in self._sprites.keys():
                sprite = self._sprites[k]
                sprite.update()
            self.update()
            current = time.time()
            delta = current - last_frame
            last_frame = current
            offset = 1 / 60 - delta
            if offset > 0:
                time.sleep(offset)

    def find(self, name):
        if name in self._sprites.keys():
            return self._sprites[name]
        for n in self._new_sprites:
            if n[0] == name:
                return n[1]
        return None

    def find_by_class(self, name):
        res = []
        for k in self._sprites.keys():
            sprite = self._sprites[k]
            if sprite.class_name == name:
                res.append(sprite)
        for n in self._new_sprites:
            if n[1].class_name == name:
                res.append(n[1])
        return res

    def instantiate(self, sprite, name):
        if name not in self._sprites.keys():
            new_sprite = sprite
            # new_sprite = copy.deepcopy(sprite)
            self._new_sprites.append((name, new_sprite))
            return new_sprite
        return None

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.input.key_status(event.key(), True)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        self.input.key_status(event.key(), False)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        pass

    def paintEvent(self, a0: QPaintEvent) -> None:
        self._painter.begin(self)
        sprites = []
        for k in self._sprites:
            sprites.append(self._sprites[k])
        sprites = sorted(sprites, key=lambda s: s.render.layer)
        for sprite in sprites:
            if not sprite.is_text:
                frame = sprite.animator.tick()
                if sprite.render.enable:
                    if frame is None:
                        frame = sprite.animator.frames[sprite.render.default_frame]
                    image = frame.toImage()
                    image = image.scaledToWidth(frame.width() * sprite.render.scale)
                    image = image.mirrored(sprite.render.flipX, False)
                    frame = QPixmap.fromImage(image)
                    self._painter.drawPixmap(
                        sprite.transform.position.x + self.width() // 2 - frame.width() // 2,
                        -sprite.transform.position.y + self.height() // 2 - frame.height() // 2,
                        frame
                    )
            elif sprite.render.enable:
                self._painter.setPen(Qt.red)
                self._painter.setFont(QFont("Arial", 20 * sprite.render.scale))
                self._painter.drawText(sprite.transform.position.x + self.width() // 2,
                                       sprite.transform.position.y + self.height() // 2,
                                       sprite.context)
        self._painter.end()

    def initialize_sprites(self):
        data, script = self.data, self.script_module
        sprites = {}
        for k in data["sprites"].keys():
            sprite = data["sprites"][k]
            if sprite["script"]["class_name"] != "":
                sprite_instance = Misc.get_sprite(script, sprite["script"]["class_name"])
            else:
                sprite_instance = Sprite()
            sprite_instance.class_name = sprite["script"]["class_name"]
            sprite_instance.input = self.input
            sprite_instance.sound = self.sound
            sprite_instance.game_application = self
            sprite_position = sprite["transform"]["position"]
            sprite_instance.transform.position = Vector2(sprite_position["x"], sprite_position["y"])
            sprite_instance.render.enable = sprite["render"]["enable"]
            sprite_instance.render.layer = sprite["render"]["layer"]
            sprite_instance.render.scale = sprite["render"]["render_scale"]
            sprite_instance.is_text = sprite["is_text"]
            if not sprite["is_text"]:
                sprite_instance.render.flipX = sprite["render"]["flipX"]
                sprite_instance.render.default_frame = sprite["render"]["default_frame"]
                sprite_instance.collision.enable = sprite["collision"]["enable"]
                sprite_instance.collision.size.x = sprite["collision"]["x_size"]
                sprite_instance.collision.size.y = sprite["collision"]["y_size"]
                sprite_instance.animator.triggers = sprite["sprite"]["triggers"]
                sprite_instance.animator.animations = sprite["sprite"]["animations"]
                sprite_instance.animator.transitions = sprite["sprite"]["transitions"]
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(sprite["sprite"]["image"]["data"]))
                slice_width = pixmap.width() // sprite["sprite"]["image"]["col"]
                slice_height = pixmap.height() // sprite["sprite"]["image"]["row"]
                for y in range(sprite["sprite"]["image"]["row"]):
                    for x in range(sprite["sprite"]["image"]["col"]):
                        frame = pixmap.copy(QRect(
                            x * slice_width, y * slice_height,
                            slice_width, slice_height
                        ))
                        sprite_instance.animator.frames.append(frame)
            else:
                sprite_instance.context = sprite["content"]
            sprite_instance.script_instance = sprite_instance
            sprites[k] = sprite_instance
        return sprites


def launch(data, script):
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = GameWindow(data, script)
    win.show()
    app.exec()