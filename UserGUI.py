from PyQt5 import uic

class MainGUI:

    def __init__(self):
        # 从文件中加载UI定义
        MainGUI.ui = uic.loadUi("UserUI/RobotUI.ui")