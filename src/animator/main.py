from gui import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QGraphicsScene
)
from PyQt5.QtGui import (
    QPixmap
)


class Animator(QMainWindow, animator.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals()
        self._currentProjectFile = ""
        self._currentProject = {}

    def _connect_signals(self):
        self.actionNewSprite.triggered.connect(self._new_project)
        self.actionOpenSprite.triggered.connect(self._open_project)
        self.actionSaveSprite.triggered.connect(self._save_project)
        self.openImageBtn.clicked.connect(self._open_image)

    def _new_project(self):
        self.setWindowTitle("Animator" + " - Project.sprite")
        if self._currentProjectFile != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "新建项目", "", "Sprite文件 (*.sprite)", options=options)
        if file_name != "":
            self._currentProjectFile = file_name
        else:
            QMessageBox.warning(self, "警告", "项目未新建。")

    def _open_project(self):
        if self._currentProjectFile != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "打开项目", "", "Sprite文件 (*.sprite)", options=options)
        if file_name != "":
            self._currentProjectFile = file_name
        else:
            QMessageBox.warning(self, "警告", "无项目打开。")

    def _save_project(self):
        if self._currentProjectFile == "":
            QMessageBox.critical(self, "错误", "当前无打开项目。")
        else:
            pass

    def _open_image(self):
        if self._currentProjectFile == "":
            QMessageBox.critical(self, "错误", "请先打开项目。")
        else:
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "PNG图片 (*.png)", options=options)
            self._currentProject["imageFile"] = file_name
            scene = QGraphicsScene()
            pixmap = QPixmap(file_name)
            if pixmap.height() > pixmap.width():
                pixmap = pixmap.scaledToHeight(self.spriteView.height())
            else:
                pixmap = pixmap.scaledToWidth(self.spriteView.width())
            scene.addPixmap(pixmap)
            self.spriteView.setScene(scene)

if __name__ == '__main__':
    app = QApplication([])
    win = Animator()
    win.show()
    app.exec()
