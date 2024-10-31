__author__ = 'Xitong Wei'

from PyQt5 import QtWidgets, QtCore
import sys

# 引入 开始界面ui 类
from start import Ui_MainWindow

# 引入游戏界面ui类
from mainform import MainWindow


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 实例化开始界面UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接信号与槽
        self.ui.pushButton.clicked.connect(self.on_button_clicked)
        self.ui.registerButton.clicked.connect(self.register_button_clicked)

    # 这里是点击注册按钮后执行的操作
    def register_button_clicked(self):
        # 点击后不会直接跳转到游戏界面
        register_userID = self.ui.lineEdit.text()
        register_password = self.ui.lineEdit_2.text()
        print("注册ID为：", register_userID, "\n注册密码为：", register_password)

        ###### 这里写数据库相关代码 ######
        # 功能：把register_userID和对应的register_password写入数据库





        ################

        print("注册成功!")  # 测试代码


    # 这里是点击登录按钮后执行的操作
    def on_button_clicked(self):
        print("登录成功!")  # 测试代码

        # 获取用户输入
        userID = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        print("ID: ", userID, "\npassword: ", password, "\n")  # 测试代码

        ######### 这里是数据库相关代码 ########
        # 功能：从数据库里读取和userID匹配的通关数据
        # 有没有可能实现“检测密码是否正确”的功能？=_=




        ############

        # 启动主游戏界面
        self.gameMainWindow = MainWindow()
        self.gameMainWindow.show()



