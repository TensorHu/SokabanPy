# run.py
__author__ = 'Zhewei Hu'

from PyQt5 import QtCore, QtWidgets
from mainform import MainWindow
import sys

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication([])
    #前面的废话没啥用
    window = MainWindow()
    #后面的废话没啥用
    sys.exit(app.exec())
