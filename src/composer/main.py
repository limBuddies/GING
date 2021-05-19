import os
import json
import shutil
import subprocess
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
    Qt, QRect
)
from PyQt5 import QtCore


class Composer(QMainWindow, composer.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals()
        self._currentProject = ""
        self._projectName = ""
        self._sprites = {}
        self._sounds = {}
        self._currentSprite = ""
        self._scene = QGraphicsScene()
        self.sceneView.setScene(self._scene)
        self._refresh_scene()
        self._refresh_inspector()
        self._debug_process = None

    # noinspection DuplicatedCode
    def _connect_signals(self):
        self.actionNew.triggered.connect(self._new_project)
        self.actionOpen.triggered.connect(self._open_project)
        self.actionSave.triggered.connect(self._save_project)
        self.actionAdd_Sprite.triggered.connect(self._add_sprite)
        self.actionAdd_Text.triggered.connect(self._add_text)
        self.actionNew_Sprite.triggered.connect(self._launch_animator)
        self.spriteList.clicked.connect(self._sprite_selection_changed)
        self.nameInput.textChanged.connect(lambda s: self._update_sprite([], s))
        self.xPosSpin.valueChanged.connect(lambda v: self._update_sprite(["transform", "position", "x"], v))
        self.yPosSpin.valueChanged.connect(lambda v: self._update_sprite(["transform", "position", "y"], v))
        self.renderCheck.stateChanged.connect(lambda v: self._update_sprite(["render", "enable"], v > 0))
        self.flipXCheck.stateChanged.connect(lambda v: self._update_sprite(["render", "flipX"], v > 0))
        self.layerSpin.valueChanged.connect(lambda v: self._update_sprite(["render", "layer"], v))
        self.defaultFrameSpin.valueChanged.connect(lambda v: self._update_sprite(["render", "default_frame"], v))
        self.scaleSpin.valueChanged.connect(lambda v: self._update_sprite(["render", "render_scale"], v))
        self.collisionCheck.stateChanged.connect(lambda v: self._update_sprite(["collision", "enable"], v > 0))
        self.xCollisionSpin.valueChanged.connect(lambda v: self._update_sprite(["collision", "x_size"], v))
        self.yCollisionSpin.valueChanged.connect(lambda v: self._update_sprite(["collision", "y_size"], v))
        self.className.textChanged.connect(lambda s: self._update_sprite(["script", "class_name"], s))
        self.textInput.textChanged.connect(lambda s: self._change_text(s))
        self.addSound.clicked.connect(self._add_sound)
        self.delSound.clicked.connect(self._del_sound)
        self.runDebugBtn.clicked.connect(self._run_project)
        self.stopDebugBtn.clicked.connect(self._stop_project)
        self.actionBuild_Folder.triggered.connect(self._build_folder)

    def _run_project(self):
        self._save_project()
        init_str = ""
        for c in os.listdir(os.path.join(self._currentProject, "Assets/Script")):
            if c.endswith(".py") and c != "__init__.py":
                class_name = c.split(".")[0]
                init_str += "from ." + class_name + " import " + class_name + "\n"
        open(os.path.join(self._currentProject, "Assets/Script/__init__.py"), "w+").write(init_str)
        os.chdir(self._currentProject)
        self._debug_process = subprocess.Popen("python " + self._projectName + ".py")

    def _stop_project(self):
        if self._debug_process is not None:
            self._debug_process.kill()
            self._debug_process = None

    def _build_folder(self):
        os.startfile(self._currentProject)

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
                self._projectName = project
                self.setWindowTitle("Composer - " + self._projectName)
                self._currentProject = folder_name
                open(os.path.join(self._currentProject, project + ".scene"), "w+").write("{}")
                os.mkdir(os.path.join(self._currentProject, "Assets"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Script"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Sprites"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Sounds"))
                os.mkdir(os.path.join(self._currentProject, "Assets/Textures"))
                core_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "../core/")
                shutil.copyfile(
                    os.path.join(core_path, "ProjectName.py"),
                    os.path.join(self._currentProject, self._projectName + ".py")
                )
                shutil.copytree(
                    os.path.join(core_path, "Runtime"),
                    os.path.join(self._currentProject, "Runtime")
                )
                shutil.copytree(
                    os.path.join(core_path, "Runtime/GING"),
                    os.path.join(self._currentProject, "Assets/Script/GING")
                )
                shutil.copyfile(
                    os.path.join(core_path, "Template.py"),
                    os.path.join(self._currentProject, "Assets/Script/Template.py")
                )
                open(os.path.join(self._currentProject, "Assets/Script/__init__.py"), "w+").close()
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
            if os.path.exists(os.path.join(folder_name, os.path.split(folder_name)[1] + ".scene")):
                self._currentProject = folder_name
                self._projectName = os.path.split(folder_name)[1]
                self.setWindowTitle("Composer - " + self._projectName)
                try:
                    project_obj = json.loads(open(os.path.join(folder_name, self._projectName + ".scene")).read())
                except ValueError:
                    return
                try:
                    self._sprites = project_obj["sprites"]
                    self._sounds = project_obj["sounds"]
                except KeyError:
                    self._sprites = {}
                    self._sounds = {}
                self._refresh_scene()
                self._refresh_inspector()
                self.statusbar.showMessage("项目已打开。")
            else:
                QMessageBox.critical(self, "错误", "非合法项目。")
        else:
            QMessageBox.warning(self, "警告", "无项目打开。")

    def _save_project(self):
        if self._currentProject != "":
            with open(os.path.join(self._currentProject, self._projectName + ".scene"), "w+") as project_file:
                project_file.write(json.dumps({
                    "sprites": self._sprites,
                    "sounds": self._sounds
                }))
            self.statusbar.showMessage("项目已保存。")
        else:
            QMessageBox.warning(self, "警告", "无项目打开。")

    @staticmethod
    def _launch_animator():
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        os.popen("python ../animator/main.py")

    def _add_sprite(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "无项目打开。")
        else:
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "添加Sprite", self._currentProject, "Sprite文件 (*.sprite)",
                                                       options=options)
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
                        "enable": True,
                        "flipX": False,
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
                self._currentSprite = sprite_name
                self._select_sprite(self._currentSprite)
                self._refresh_scene()
                self._refresh_inspector()
                self.statusbar.showMessage("Sprite已添加。")
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
                    "enable": True,
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
            self.statusbar.showMessage("文本已添加。")

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
                self._refresh_scene()

    def _refresh_scene(self):
        self._scene.clear()
        self.spriteList.clear()
        for k in self._sprites.keys():
            sprite = self._sprites[k]
            self.spriteList.addItem(k)
            if not sprite["is_text"]:
                if sprite["render"]["enable"]:
                    sprite_path = os.path.join(self._currentProject, sprite["path"])
                    sprite_obj = json.loads(open(sprite_path).read())
                    image_path = os.path.join(os.path.split(sprite_path)[0], sprite_obj["image"]["path"])
                    pixmap = QPixmap(image_path)
                    slice_col = sprite_obj["image"]["col"]
                    slice_row = sprite_obj["image"]["row"]
                    slice_width = pixmap.width() // slice_col
                    slice_height = pixmap.height() // slice_row
                    slice_index = sprite["render"]["default_frame"]
                    pixmap = pixmap.copy(
                        QRect(
                            (slice_index % slice_col) * slice_width,
                            (slice_index // slice_col) * slice_height,
                            slice_width, slice_height))
                    pixmap = pixmap.scaledToWidth(int(pixmap.width() * sprite["render"]["render_scale"]))
                    pixmap = QPixmap.fromImage(pixmap.toImage().mirrored(sprite["render"]["flipX"], False))
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
                if sprite["render"]["enable"]:
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
        try:
            if self._currentSprite != "":
                sprite = self._sprites[self._currentSprite]
                self.nameInput.setText(self._currentSprite)
                self.xPosSpin.setValue(sprite["transform"]["position"]["x"])
                self.yPosSpin.setValue(sprite["transform"]["position"]["y"])
                self.renderCheck.setChecked(sprite["render"]["enable"])
                self.layerSpin.setValue(sprite["render"]["layer"])
                if not sprite["is_text"]:
                    sprite_obj = json.loads(open(os.path.join(self._currentProject, sprite["path"])).read())
                    frame_max = sprite_obj["image"]["col"] * sprite_obj["image"]["row"]
                    self.defaultFrameSpin.setMaximum(frame_max - 1)
                    self.flipXCheck.setChecked(sprite["render"]["flipX"])
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
            self.soundList.clear()
            for k in self._sounds.keys():
                self.soundList.addItem(k)
        except Exception as e:
            QMessageBox.critical(self, "", repr(e))

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

    def _add_sound(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "无项目打开。")
        else:
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "添加音频", self._currentProject, "WAV文件 (*.wav)",
                                                       options=options)
            if file_name != "":
                sound_name = os.path.split(file_name)[1].split(".")[0]
                if sound_name not in self._sounds.keys():
                    self._sounds[sound_name] = os.path.relpath(file_name, self._currentProject)
                    self._refresh_inspector()
                    self.statusbar.showMessage("声音已添加。")
                else:
                    QMessageBox.critical(self, "错误", "音频已存在。")

    def _del_sound(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "无项目打开。")
        else:
            if len(self.soundList.selectedIndexes()) > 0:
                del self._sounds[self.soundList.selectedItems()[0].text()]
                self._refresh_inspector()
                self.statusbar.showMessage("声音已删除。")


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = Composer()
    win.show()
    app.exec()
