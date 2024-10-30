# run.py
__author__ = 'Zhewei Hu'

from PyQt5 import QtCore, QtWidgets
from mainform import MainWindow
import sys
import pygame
from startwindow import MyMainWindow



if __name__ == "__main__":
    # 整点bgm
    pygame.mixer.init()  # 初始化pygame音频模块
    pygame.mixer.music.load("gamemusic.mp3")  # 替换为音乐文件路径（两个都很适合嗯
    pygame.mixer.music.play(-1)  # -1表示循环播放

    # 这里改成直接启动getID里的开始界面
    # 设置为: 点击开始界面的“确认”后，才进入到主游戏界面
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MyMainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # app2 = QtWidgets.QApplication([])
    # app2 = QtWidgets.QApplication(sys.argv)
    # 前面的废话没啥用
    # window = MainWindow()
    # window.show()
    # 后面的废话没啥用
    # sys.exit(app2.exec())




