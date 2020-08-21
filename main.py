import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from UserGUI import MainGUI
RobotUI = QApplication([])
GUI=MainGUI()
GUI.ui.show()
RobotUI.exec_()