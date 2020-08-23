import sys
from PyQt5 import uic
import serial
import serial.tools.list_ports
from threading import Thread,Lock
import time
from PyQt5.QtCore import *
OpenSerSingal=0
UartStr=""
RecFlag=0
class MainGUI:
    def __init__(self):
        super(MainGUI, self).__init__()
        MainGUI.ser = serial.Serial()
        MainGUI.init(self)
        # 从文件中加载UI定义
        MainGUI.ui = uic.loadUi("UserUI/RobotUI.ui")
        MainGUI.ui.ReFlashUart.clicked.connect(MainGUI.ReFlashUart)
        MainGUI.ui.OpenUart.clicked.connect(MainGUI.OpenSerial)
        MainGUI.ui.UartSendButtom.clicked.connect(MainGUI.SendMessage)
        MainGUI.ui.ClearButtom.clicked.connect(MainGUI.ClearButtom)


    def ClearButtom(self):
        MainGUI.ui.UartRec.clear()
    def init(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.ReFlashRec)
        self.timer.start(100)
    def ReFlashRec(self):
        global lock
        global UartStr,RecFlag
        if RecFlag==1:
            MainGUI.ui.UartRec.append(str(UartStr))
            RecFlag=0
    def ReFlashUart(self):
        global PortList
        MainGUI.ui.UartList.clear()
        PortList = list(serial.tools.list_ports.comports())
        for i in list(PortList) :
            MainGUI.ui.UartList.addItem(i[1])
    def UartPrintGUI(self,text):
        MainGUI.ui.UartRec.append(str(text))        
    def OpenSerial(self):
        global PortList,OpenSerSingal
        if  OpenSerSingal==0 :
            for i in list(serial.tools.list_ports.comports()):
                if MainGUI.ui.UartList.currentText() == i[1] :
                    MainGUI.ser.baudrate=115200
                    MainGUI.ser.port=i[0]
                    
                    try:
                        MainGUI.ser.open()
                    except Exception:
                        print("发生了什么错误qaq")
                    if MainGUI.ser.isOpen() :
                        MainGUI.ui.UartStates.setText(i[1]+"已经打开")
                        MainGUI.ui.UartSendButtom.setEnabled(True)
                        MainGUI.ui.OpenUart.setEnabled(False)
                        OpenSerSingal=1
                    else :
                        MainGUI.ui.UartStates.setText(i[1]+"未打开")
                        OpenSerSingal=0
    def UartRecBegin(self):
        global lock
        thread = Thread(target = MainGUI.Run)
        lock = Lock()
        thread.start()
    def Run():
        global lock
        global UartStr,RecFlag
        while True:
            lock.acquire()
            time.sleep(0.1)
            if MainGUI.ser.isOpen():
                count = MainGUI.ser.inWaiting()
                if count!=0:
                    UartStr=MainGUI.ser.read(count)
                    UartStr=UartStr.decode('iso-8859-1')
                    RecFlag=1

                    #MainGUI.UartPrint.UartPrintStr.emit(UartStr)
                    #MainGUI.ui.UartRec.append(UartStr) 
                    MainGUI.ser.flushInput()
                else :
                    pass
                
                
            lock.release()

    def SendMessage(self):
        MainGUI.ser.write(MainGUI.ui.UartSend.toPlainText().encode('utf-8'))