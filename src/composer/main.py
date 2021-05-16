import os
import json
from gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QGraphicsScene
)
from PyQt5.QtGui import (
    QPixmap,
    QPen,
    QFont
)
from PyQt5.QtCore import (
    QLineF,
    QRectF,
    Qt
)
from PyQt5 import QtCore


class Composer(QMainWindow, composer.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals()
        self._currentProject = ""
        self._sprites = {}
        self._sounds = {}
        self._currentSprite = ""
        self._scene = QGraphicsScene()
        self.sceneView.setScene(self._scene)
        self._refresh_scene()
        self._refresh_inspector()

    # noinspection DuplicatedCode
    def _connect_signals(self):
        self.actionNew.triggered.connect(self._new_project)
        self.actionOpen.triggered.connect(self._open_project)
        self.actionSave.triggered.connect(self._save_project)
        self.actionSaveAs.triggered.connect(self._save_project_as)
        self.actionAdd_Sprite.triggered.connect(self._add_sprite)
        self.actionAdd_Text.triggered.connect(self._add_text)
        self.actionNew_Sprite.triggered.connect(self._launch_animator)
        self.spriteList.currentRowChanged.connect(self._sprite_selection_changed)
        self.nameInput.textChanged.connect(lambda s: self._update_sprite([], s))
        self.xPosSpin.valueChanged.connect(lambda v: self._update_sprite(["transform", "position", "x"], v))
        self.yPosSpin.valueChanged.connect(lambda v: self._update_sprite(["transform", "position", "y"], v))
        self.layerSpin.valueChanged.connect(lambda v: self._update_sprite(["render", "layer"], v))
        self.defaultFrameSpin.valueChanged.connect(lambda v: self._update_sprite(["render", "default_frame"], v))
        self.scaleSpin.valueChanged.connect(lambda v: self._update_sprite(["render", "render_scale"], v))
        self.collisionCheck.stateChanged.connect(lambda v: self._update_sprite(["collision", "enable"], v > 0))
        self.xCollisionSpin.valueChanged.connect(lambda v: self._update_sprite(["collision", "x_size"], v))
        self.yCollisionSpin.valueChanged.connect(lambda v: self._update_sprite(["collision", "y_size"], v))
        self.className.textChanged.connect(lambda s: self._update_sprite(["script", "class_name"], s))
        self.textInput.textChanged.connect(lambda s: self._change_text(s))

    def _new_project(self):
        if self._currentProject != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        folder_name = QFileDialog.getExistingDirectory(self, "新建项目", "./", options=options)
        if folder_name != "":
            if os.listdir(folder_name):
                QMessageBox.critical(self, "错误", "文件夹不为空")
            else:
                project = os.path.split(folder_name)[1]
                self.setWindowTitle("Composer - " + project)
                self._currentProject = folder_name
                open(os.path.join(self._currentProject, project + ".scene"), "w+").close()
                os.mkdir(os.path.join(self._currentProject, "Assets"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Scripts"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Sprites"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Textures"))
                self.statusbar.showMessage("项目已新建。")
        else:
            QMessageBox.warning(self, "警告", "项目未新建。")

    def _open_project(self):
        if self._currentProject != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        folder_name = QFileDialog.getExistingDirectory(self, "打开项目", "./", options=options)
        if folder_name != "":
            self._currentProject = folder_name
            self.setWindowTitle("Composer - " + self._currentProject)
        else:
            QMessageBox.warning(self, "警告", "无项目打开。")

    def _save_project(self):
        pass

    def _save_project_as(self):
        pass

    def _save_project_structure(self):
        sprite_sturcture = {
            "is_text": False,
            "data": "",
            "transform": {
                "position": {
                    "x": 0.0,
                    "y": 0.0
                }
            },
            "render": {
                "layer": 0,
                "default_frame": 0,
                "render_scale": 0.0
            },
            "collision": {
                "enable": False,
                "x_size": 0.00,
                "y_size": 0.00
            },
            "script": {
                "class_name": ""
            }
        }
        project_structure = {
            "sprites": {
                "UniqueSpriteName": sprite_sturcture
            },
            "sounds": {
                "soundName": "soundFilePath"
            }
        }
        print(project_structure)

    @staticmethod
    def _launch_animator():
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        os.popen("python ../animator/main.py")

    def _add_sprite(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "无项目打开。")
        else:
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "添加Sprite", "", "Sprite文件 (*.sprite)", options=options)
            if file_name != "":
                sprite_name = os.path.split(file_name)[1].split(".")[0]
                while sprite_name in self._sprites.keys():
                    sprite_name += "#"
                self._sprites[sprite_name] = {
                    "is_text": False,
                    "path": os.path.relpath(file_name, self._currentProject),
                    "transform": {
                        "position": {
                            "x": 0.0,
                            "y": 0.0
                        }
                    },
                    "render": {
                        "layer": 0,
                        "default_frame": 0,
                        "render_scale": 1.0
                    },
                    "collision": {
                        "enable": False,
                        "x_size": 0.00,
                        "y_size": 0.00
                    },
                    "script": {
                        "class_name": ""
                    }
                }
                sprite_path = os.path.join(self._currentProject, file_name)
                image_path = os.path.join(os.path.split(sprite_path)[0],
                                          json.loads(open(sprite_path).read())["image"]["path"])
                self._sprites[sprite_name]["image_path"] = image_path
                self._currentSprite = sprite_name
                self._select_sprite(self._currentSprite)
                self._refresh_scene()
                self._refresh_inspector()
            else:
                QMessageBox.warning(self, "警告", "Sprite未添加。")

    def _add_text(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "无项目打开。")
        else:
            name = "New Text"
            while name in self._sprites.keys():
                name += "#"
            self._sprites[name] = {
                "is_text": True,
                "content": "",
                "transform": {
                    "position": {
                        "x": 0.0,
                        "y": 0.0
                    }
                },
                "render": {
                    "layer": 0,
                    "default_frame": 0,
                    "render_scale": 1.0
                },
                "collision": {
                    "enable": False,
                    "x_size": 0.00,
                    "y_size": 0.00
                },
                "script": {
                    "class_name": ""
                }
            }
            self._currentSprite = name
            self._select_sprite(self._currentSprite)
            self._refresh_scene()
            self._refresh_inspector()

    def _select_sprite(self, sprite):
        if sprite in self._sprites.keys():
            self.spriteList.setCurrentRow(list(self._sprites.keys()).index(sprite))

    def _sprite_selection_changed(self):
        if len(self.spriteList.selectedIndexes()) > 0:
            self._currentSprite = self.spriteList.currentItem().text()
            self._refresh_inspector()

    def _change_text(self, text):
        if self._currentSprite != "":
            if self._sprites[self._currentSprite]["is_text"]:
                self._sprites[self._currentSprite]["content"] = text

    def _refresh_scene(self):
        self._scene.clear()
        self.spriteList.clear()
        for k in self._sprites.keys():
            sprite = self._sprites[k]
            self.spriteList.addItem(k)
            if not sprite["is_text"]:
                pixmap = QPixmap(sprite["image_path"])
                pixmap = pixmap.scaledToWidth(int(pixmap.width() * sprite["render"]["render_scale"]))
                pixmap_item = self._scene.addPixmap(pixmap)
                pixmap_item.setPos(sprite["transform"]["position"]["x"], -sprite["transform"]["position"]["y"])
                pixmap_item.moveBy(pixmap.width() // -2, pixmap.height() // -2)
                pixmap_item.moveBy(self.sceneView.width() // 2, self.sceneView.height() // 2)
                pixmap_item.setZValue(sprite["render"]["layer"])
                if sprite["collision"]["enable"]:
                    pen = QPen(Qt.green, 1, Qt.SolidLine)
                    c_width = sprite["collision"]["x_size"]
                    c_height = sprite["collision"]["y_size"]
                    collision_item = self._scene.addRect(QRectF(
                        sprite["transform"]["position"]["x"] - c_width // 2,
                        -sprite["transform"]["position"]["y"] - c_height // 2,
                        c_width,
                        c_height
                    ), pen)
                    collision_item.moveBy(self.sceneView.width() // 2, self.sceneView.height() // 2)
                    collision_item.setZValue(sprite["render"]["layer"])
            else:
                text_item = self._scene.addText(
                    sprite["content"] if len(sprite["content"]) > 0 else k, QFont("Arial", 20))
                text_item.setScale(sprite["render"]["render_scale"])
                text_item.setPos(sprite["transform"]["position"]["x"], -sprite["transform"]["position"]["y"])
                text_item.moveBy(self.sceneView.width() // 2, self.sceneView.height() // 2)
                text_item.setZValue(sprite["render"]["layer"])
                text_item.setDefaultTextColor(Qt.red)
        pen = QPen(Qt.darkGray, 1, Qt.DotLine)
        self._scene.addLine(
            QLineF(
                0, self.sceneView.height() / 2,
                self.sceneView.width(), self.sceneView.height() / 2), pen).setZValue(9999)
        self._scene.addLine(
            QLineF(
                self.sceneView.width() / 2, 0,
                self.sceneView.width() / 2, self.sceneView.height()), pen).setZValue(9999)

    def _refresh_inspector(self):
        if self._currentSprite != "":
            sprite = self._sprites[self._currentSprite]
            self.nameInput.setText(self._currentSprite)
            self.xPosSpin.setValue(sprite["transform"]["position"]["x"])
            self.yPosSpin.setValue(sprite["transform"]["position"]["y"])
            self.layerSpin.setValue(sprite["render"]["layer"])
            self.defaultFrameSpin.setValue(sprite["render"]["default_frame"])
            self.scaleSpin.setValue(sprite["render"]["render_scale"])
            self.collisionCheck.setChecked(sprite["collision"]["enable"])
            self.xCollisionSpin.setValue(sprite["collision"]["x_size"])
            self.yCollisionSpin.setValue(sprite["collision"]["y_size"])
            self.className.setText(sprite["script"]["class_name"])
        else:
            self.nameInput.clear()
            self.xPosSpin.clear()
            self.yPosSpin.clear()
            self.layerSpin.clear()
            self.defaultFrameSpin.clear()
            self.scaleSpin.clear()
            self.collisionCheck.setChecked(False)
            self.xCollisionSpin.clear()
            self.yCollisionSpin.clear()
            self.className.clear()

    def _update_sprite(self, path, value):
        if len(self.nameInput.text()) != 0:
            if self._currentSprite != "":
                if len(path) == 0:
                    if value != self._currentSprite:
                        self._sprites[value] = self._sprites[self._currentSprite]
                        del self._sprites[self._currentSprite]
                        self._currentSprite = value
                else:
                    self._update_sprite_r(self._sprites[self._currentSprite], path, value)
        self._refresh_scene()

    def _update_sprite_r(self, obj, path, value):
        if len(path) == 1:
            obj[path[0]] = value
        else:
            self._update_sprite_r(obj[path[0]], path[1:], value)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = Composer()
    win.show()
    app.exec()
