# mainform.py
__author__ = 'Zhewei Hu'

from PyQt5 import QtWidgets, uic
from display import Display

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./mainwindow.ui")
        self.ui.show()
        self.load_sav()
        # 按钮关联动作
        self.ui.pushButton.clicked.connect(self.start_level)

    def start_level(self):
        d = Display()
        d.load_level(self.ui.spinBox.value())
        self.load_sav()

    def load_sav(self):
        """
            读取当前关卡进度
        """
        sav_file_path = "./level.sav"
        with open(sav_file_path, "r") as f:
            max_unlock_level = int(f.readline().strip("\n"))
        # 更新spinbox的值与最大值
        self.ui.spinBox.setMaximum(max_unlock_level)
        self.ui.spinBox.setValue(max_unlock_level)
