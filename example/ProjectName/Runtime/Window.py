from .gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow
)
from PyQt5 import QtCore, QtGui


class GameWindow(QMainWindow, window.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        pass

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        pass


def launch():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = GameWindow()
    win.show()
    app.exec()
