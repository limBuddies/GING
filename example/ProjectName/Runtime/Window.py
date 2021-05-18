from .gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)
from PyQt5 import QtCore


class GameWindow(QMainWindow, window.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


def show():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = GameWindow()
    win.show()
    app.exec()
