# run.py
__author__ = 'Zhewei Hu'

from PyQt5 import QtCore, QtWidgets
from mainform import MainWindow
import sys

if __name__ == "__main__":
    # 整点bgm
    pygame.mixer.init()  # 初始化pygame音频模块
    pygame.mixer.music.load("gamemusic.mp3")  # 替换为音乐文件路径（两个都很适合嗯
    pygame.mixer.music.play(-1)  # -1表示循环播放
    
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])
    #前面的废话没啥用
    window = MainWindow()
    #后面的废话没啥用
    sys.exit(app.exec())
