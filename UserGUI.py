import sys
from PyQt5 import uic
import serial
import serial.tools.list_ports

class MainGUI:

    def __init__(self):
        # 从文件中加载UI定义
        MainGUI.ui = uic.loadUi("UserUI/RobotUI.ui")
        MainGUI.ui.ReFlashUart.clicked.connect(MainGUI.ReFlashUart)
        MainGUI.ui.OpenUart.clicked.connect(MainGUI.OpenSerial)
    def ReFlashUart(self):
        global PortList
        MainGUI.ui.UartList.clear()
        PortList = list(serial.tools.list_ports.comports())
        for i in list(PortList) :
            MainGUI.ui.UartList.addItem(i[1])
            
    def OpenSerial(self):
        global PortList
        for i in list(PortList):
            if MainGUI.ui.UartList.currentText() == i[1] :
                try:
                    SlaveSer=serial.Serial(i[0],115200,timeout=60)
                    #SlaveSer=serial.Serial("/dev/ttyACM0",115200,timeout=60)
                except Exception:
                    print("发生了什么错误qaq")
                break
        SlaveSer.write("123456".encode('utf-8'))