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
from PyQt5 import QtCore
from PyQt5.QtCore import (
    QRectF,
    Qt
)
import base64
import json


class Animator(QMainWindow, animator.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals()
        self._currentProject = ""
        self._imageFile = ""
        self._imageData = ""
        self._slice_col = 0
        self._slice_row = 0
        self._triggers = []
        self._anime = {}
        self._transitions = []
        self._scene = QGraphicsScene()
        self.spriteView.setScene(self._scene)
        self._pixmap = None

    # noinspection DuplicatedCode
    def _connect_signals(self):
        self.actionNewSprite.triggered.connect(self._new_project)
        self.actionOpenSprite.triggered.connect(self._open_project)
        self.actionSaveSprite.triggered.connect(self._save_project)
        self.actionSaveSpriteAs.triggered.connect(self._save_project_as)
        self.openImageBtn.clicked.connect(self._open_image)
        self.sliceBtn.clicked.connect(self._cut_image)
        self.addTriggerBtn.clicked.connect(self._add_trigger)
        self.delTriggerBtn.clicked.connect(self._del_trigger)
        self.addAnimeBtn.clicked.connect(self._add_anime)
        self.delAnimeBtn.clicked.connect(self._del_anime)
        self.addTransitionBtn.clicked.connect(self._add_transition)
        self.delTransitionBtn.clicked.connect(self._del_transition)

    def _new_project(self):
        if self._currentProject != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "新建项目", "", "Sprite文件 (*.sprite)", options=options)
        if file_name != "":
            self._currentProject = file_name if file_name.endswith(".sprite") else file_name + ".sprite"
            self.setWindowTitle("Animator" + " - " + self._currentProject)
            open(self._currentProject,"w+")
            self.statusbar.showMessage("项目已新建。")
            self.tabs.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "警告", "项目未新建。")

    def _open_project(self):
        if self._currentProject != "":
            reply = QMessageBox.question(self, "保存", "是否保存当前项目更改？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._save_project()
        options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "打开项目", "", "Sprite文件 (*.sprite)", options=options)
        if file_name != "":
            self._currentProject = file_name
            self.setWindowTitle("Animator" + " - " + self._currentProject)
            project = json.loads(open(self._currentProject).read())
            self._imageData = project["image"]["data"]
            self._slice_col = project["image"]["col"]
            self._slice_row = project["image"]["row"]
            self._triggers = project["triggers"]
            self._anime = project["animations"]
            self._transitions = project["transitions"]
            self._reload_image()
            self.colSpin.setValue(self._slice_col)
            self.rowSpin.setValue(self._slice_row)
            self._cut_image()
            self._refresh()
            self.statusbar.showMessage("项目已打开。")
            self.tabs.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "警告", "无项目打开。")

    def _save_project(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "当前无打开项目。")
        else:
            with open(self._currentProject, "w") as project:
                project.write(json.dumps({
                    "image": {
                        "data": self._imageData,
                        "col": self._slice_col,
                        "row": self._slice_row
                    },
                    "triggers": self._triggers,
                    "animations": self._anime,
                    "transitions": self._transitions
                }))
            self.statusbar.showMessage("项目已保存。")

    def _save_project_as(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "当前无打开项目。")
        else:
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "另存项目", "", "Sprite文件 (*.sprite)", options=options)
            if file_name != "":
                self._currentProject = file_name if file_name.endswith(".sprite") else file_name + ".sprite"
                self.setWindowTitle("Animator" + " - " + self._currentProject)
                with open(self._currentProject, "w") as project:
                    project.write(json.dumps({
                        "image": {
                            "data": self._imageData,
                            "col": self._slice_col,
                            "row": self._slice_row
                        },
                        "triggers": self._triggers,
                        "animations": self._anime,
                        "transitions": self._transitions
                    }))
                self.statusbar.showMessage("项目已另存。")
            else:
                QMessageBox.warning(self, "警告", "项目未另存。")

    def _open_image(self):
        if self._currentProject == "":
            QMessageBox.critical(self, "错误", "请先打开项目。")
        else:
            options = int(QFileDialog.Options()) | QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "PNG图片 (*.png)", options=options)
            self._imageFile = file_name
            self._imageData = base64.b64encode(open(self._imageFile, "rb").read()).decode("utf-8")
            self._scene.clear()
            pixmap = QPixmap(file_name)
            if pixmap.height() > pixmap.width():
                self._pixmap = pixmap.scaledToHeight(self.spriteView.height())
            else:
                self._pixmap = pixmap.scaledToWidth(self.spriteView.width())
            self._scene.addPixmap(self._pixmap)
            self.statusbar.showMessage("图片已载入。")

    def _cut_image(self):
        if self.rowSpin.text() == "0" or self.colSpin.text() == "0":
            QMessageBox.critical(self, "错误", "请修改切分的行数及列数")
        else:
            # 此处利用spriteView窗口中是否打开了图片判断点击切分按钮能否做出切分图片的响应
            if self._currentProject == "":
                QMessageBox.critical(self, "错误", "未打开图片不能进行切割")
            else:
                self._reload_image()
                # 这里将模拟切分图片，根据用户输入的行列数来划线分割，并给切割后的每个图排序号
                slice_x = int(self.colSpin.text())
                slice_y = int(self.rowSpin.text())
                self._slice_col = slice_x
                self._slice_row = slice_y
                slice_width = self._pixmap.width() // slice_x
                slice_height = self._pixmap.height() // slice_y
                pen = QPen(Qt.red, 2, Qt.DashLine)
                font = QFont("Arial", 30)
                for x in range(slice_x):
                    for y in range(slice_y):
                        self._scene.addRect(
                            QRectF(x * slice_width, y * slice_height, slice_width, slice_height),
                            pen)
                        index = self._scene.addText(str(y * slice_x + x), font)
                        index.moveBy(x * slice_width + 5, y * slice_height + 5)
                        index.setDefaultTextColor(Qt.red)
                self.statusbar.showMessage("图片已切分。")

    def _add_trigger(self):
        if self.triggerName.text() == "":
            QMessageBox.critical(self, "错误", "请先输入所要添加触发器的名称")
        else:
            if self.triggerName.text() in self._triggers:
                QMessageBox.critical(self, "错误", "该触发器已经存在")
            else:
                self._triggers.append(self.triggerName.text())
                self._refresh()
                self.statusbar.showMessage("触发器已添加。")

    def _del_trigger(self):
        if len(self.triggerList.selectedItems()) != 0:
            for i in self.triggerList.selectedIndexes():
                del self._triggers[i.row()]
            self._refresh()
            self.statusbar.showMessage("触发器已删除。")
        else:
            if self.triggerName.text() == "":
                QMessageBox.critical(self, "错误", "请先输入所要删除的触发器的名称")
            else:

                if self.triggerName.text() in self._triggers:
                    # 根据触发器名称找出触发器在项目触发器的列表当中的index值来删除该触发器
                    del self._triggers[self._triggers.index(self.triggerName.text())]
                    self._refresh()
                    self.statusbar.showMessage("触发器已删除。")
                else:
                    QMessageBox.critical(self, "错误", "该触发器并不存在!")

    def _add_anime(self):
        if self.animeName.text() == "":
            QMessageBox.critical(self, "错误", "请先输入所要加入动画片段的名称")
        else:
            # 将动画片段的信息存储起来并在窗口上显示出来
            if self.animeName.text() in self._anime.keys():
                pass
            else:
                self._anime[self.animeName.text()] = {
                    "from": self.fromSpin.text(),
                    "to": self.toSpin.text(),
                    "interval": self.intervalSpin.text()
                }
                self._refresh()
                self.statusbar.showMessage("动画片段已添加。")

    def _del_anime(self):
        if len(self.animeList.selectedItems()) != 0:
            for i in self.animeList.selectedIndexes():
                del self._anime[list(self._anime.keys())[i.row()]]
            self._refresh()
            self.statusbar.showMessage("动画片段已删除。")
        else:
            if self.animeName.text() == "":
                QMessageBox.critical(self, "错误", "请先输入所要删除动画片段的名称")
            else:
                if self.animeName.text() in self._anime.keys():
                    del self._anime[self.animeName.text()]
                    self._refresh()
                    self.statusbar.showMessage("动画片段已删除。")
                else:
                    QMessageBox.critical(self, "错误", "该动画片段不存在")

    def _add_transition(self):
        if self.fromCombo.currentText() == "":
            QMessageBox.critical(self, "错误", "请先选择起始状态")
        elif self.toCombo.currentText() == "":
            QMessageBox.critical(self, "错误", "请先选择目标状态")
        elif self.triggerCombo.currentText() == "":
            QMessageBox.critical(self, "错误", "请先选择所要指定的触发器")
        else:
            if self.fromCombo.currentText() == self.toCombo.currentText():
                QMessageBox.critical(self, "错误", "起始状态与目标状态不能相同")
            else:
                for k in self._transitions:
                    if k["start"] == self.fromCombo.currentText() and \
                            k["end"] == self.toCombo.currentText() and \
                            k["trigger"] == self.triggerCombo.currentText():
                        QMessageBox.critical(self, "错误", "该状态转移已存在")
                        return
                self._transitions.append({
                    "start": self.fromCombo.currentText(),
                    "end": self.toCombo.currentText(),
                    "trigger": self.triggerCombo.currentText()
                })
                self._refresh()
                self.statusbar.showMessage("状态转移已添加。")

    def _del_transition(self):
        for i in self.transitionList.selectedIndexes():
            del self._transitions[i.row()]
        self._refresh()
        self.statusbar.showMessage("状态转移已删除。")

    def _refresh(self):
        self.triggerList.clear()
        self.triggerList.addItems(["  " + i for i in self._triggers])
        self.animeList.clear()
        for k in self._anime.keys():
            self.animeList.addItem("------------------------" + "\n" +
                                   "  动画名称：" + k + "\n" +
                                   "  开始帧:" + self._anime[k]["from"] + "\n" +
                                   "  结束帧:" + self._anime[k]["to"] + "\n" +
                                   "  间隔:" + self._anime[k]["interval"] + "ms" + "\n" +
                                   "------------------------")
        self.transitionList.clear()
        for j in self._transitions:
            self.transitionList.addItem("------------------------" + "\n" +
                                        "  起始状态：" + j["start"] + "\n" +
                                        "  目标状态:" + j["end"] + "\n" +
                                        "  触发器:" + j["trigger"] + "\n" +
                                        "------------------------")
        self.triggerName.clear()
        self.animeName.clear()
        self.fromSpin.clear()
        self.toSpin.clear()
        self.intervalSpin.clear()
        self.fromCombo.clear()
        self.fromCombo.addItem("enter")
        self.fromCombo.addItems(self._anime.keys())
        self.toCombo.clear()
        self.toCombo.addItems(self._anime.keys())
        self.triggerCombo.clear()
        self.triggerCombo.addItems(self._triggers)

    def _reload_image(self):
        self._scene.clear()
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(self._imageData))
        if pixmap.height() > pixmap.width():
            self._pixmap = pixmap.scaledToHeight(self.spriteView.height())
        else:
            self._pixmap = pixmap.scaledToWidth(self.spriteView.width())
        self._scene.addPixmap(self._pixmap)
        self.statusbar.showMessage("图片已载入。")


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    win = Animator()
    win.show()
    app.exec()
