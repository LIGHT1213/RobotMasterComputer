import sys
from PyQt5 import uic
import serial
import serial.tools.list_ports
from threading import Thread,Lock
#from PySide2.QtCore import Signal,QObject
#from PyQt5.QtCore import QObject
import time
from PyQt5.QtCore import *
OpenSerSingal=0
class MySignals(QObject):
    UartPrintStr = pyqtSignal(str)
class MainGUI:
    def __init__(self):
        # 从文件中加载UI定义
        MainGUI.ui = uic.loadUi("UserUI/RobotUI.ui")
        MainGUI.ui.ReFlashUart.clicked.connect(MainGUI.ReFlashUart)
        MainGUI.ui.OpenUart.clicked.connect(MainGUI.OpenSerial)
        MainGUI.ui.UartSendButtom.clicked.connect(MainGUI.SendMessage)

        MainGUI.UartPrint=MySignals()
        MainGUI.UartPrint.UartPrintStr.connect(MainGUI.UartPrintGUI)
    def ReFlashUart(self):
        global PortList
        MainGUI.ui.UartList.clear()
        PortList = list(serial.tools.list_ports.comports())
        for i in list(PortList) :
            MainGUI.ui.UartList.addItem(i[1])
    def UartPrintGUI(self,text):
        MainGUI.ui.UartRec.append=(str(text))        
    def OpenSerial(self):
        global PortList,SlaveSer,OpenSerSingal
        if  OpenSerSingal==0 :
            for i in list(PortList):
                if MainGUI.ui.UartList.currentText() == i[1] :
                    try:
                        SlaveSer=serial.Serial(i[0],115200,timeout=60)
                        #SlaveSer=serial.Serial("/dev/ttyACM0",115200,timeout=60)
                    except Exception:
                        print("发生了什么错误qaq")
                    if SlaveSer.isOpen() :
                        MainGUI.ui.UartStates.setText(i[1]+"已经打开")
                        OpenSerSingal=1
                    else :
                        MainGUI.ui.UartStates.setText(i[1]+"未打开")
                        OpenSerSingal=0
        return SlaveSer
        #SlaveSer.write("123456".encode('utf-8'))
    def UartRecBegin(self):
        global lock
        def Run(self):
            global lock
            ser=self.OpenSerial()
            while True:
                lock.acquire()
                if ser.isOpen():
                    count = ser.inWaiting()
                    if count!=0:
                        UartStr=ser.read(count)
                    else :
                        print("串口没开")
                    self.UartPrint.UartPrintStr.emit(UartStr)
                    SlaveSer.flushInput()
                lock.release()
        thread = Thread(target = self.Run)
        lock = Lock()
        thread.start()


    def SendMessage(self):
        global SlaveSer
        SlaveSer.write(MainGUI.ui.UartSend.toPlainText().encode('utf-8'))
""" class UartRecThread(QThread):
    _single=pyqtSignal(str)
    def __init__(self,ser):
        super(MyThread,self).__init__()
        self.ser=SlaveSer
 
    def run(self):
        while True:
            try:
                while self.ser!=None and self.ser.is_open==True:
                    count=self.ser.in_waiting
                    if count>0:
                        UartStr=self.ser.read(count)
                        self.UartPrint.UartPrintStr.emit(UartStr)
                        self.ser.flushInput()
            except:
                pass """