from gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)
from PyQt5 import QtCore


class Composer(QMainWindow, composer.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        sprite_sturcture = {
            "name": "Unique sprite name",
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
            "sprites": [sprite_sturcture],
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
