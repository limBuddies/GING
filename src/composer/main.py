from gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog
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

    def _connect_signals(self):
        self.actionNew.triggered.connect(self._new_project)
        self.actionOpen.triggered.connect(self._open_project)
        self.actionSave.triggered.connect(self._save_project)
        self.actionSaveAs.triggered.connect(self._save_project_as)

    def _new_project(self):
        if self._currentProject != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "新建项目", "", "Scene文件 (*.scene)", options=options)
            if file_name != "":
                self._currentProject = file_name if file_name.endswith(".scene") else file_name + ".scene"
                self.setWindowTitle("Composer - " + self._currentProject)
                open(self._currentProject, "w+").close()
                self.statusbar.showMessage("项目已新建。")
            else:
                QMessageBox.warning(self, "警告", "项目未新建。")

    def _open_project(self):
        if self._currentProject != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "打开项目", "", "Scene文件 (*.scene)", options=options)
        if file_name != "":
            self._currentProject = file_name
            self.setWindowTitle("Animator" + " - " + self._currentProject)
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


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = Composer()
    win.show()
    app.exec()
