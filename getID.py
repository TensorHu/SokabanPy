from PyQt5 import QtWidgets

# 引入 开始界面ui 类
from start import Ui_MainWindow


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 实例化UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接信号与槽
        self.ui.pushButton.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        # 这里是点击确认按钮后执行的操作
        # 点击确认后可以直接跳转到游戏界面
        print("yes!")  # 测试代码

        # 获取用户输入
        userID = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        print("ID: ", userID, "\npassword: ", password, "\n")  # 测试代码