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
        super(MainGUI, self).__init__()
        MainGUI.ser = serial.Serial()

        # 从文件中加载UI定义
        MainGUI.ui = uic.loadUi("UserUI/RobotUI.ui")
        MainGUI.ui.ReFlashUart.clicked.connect(MainGUI.ReFlashUart)
        MainGUI.ui.OpenUart.clicked.connect(MainGUI.OpenSerial)
        MainGUI.ui.UartSendButtom.clicked.connect(MainGUI.SendMessage)

        MainGUI.UartPrint=MySignals()
        MainGUI.UartPrint.UartPrintStr.connect(MainGUI.UartPrintGUI)
    def init(self):
        MainGUI.timer = QTimer(self)
        MainGUI.timer.timeout.connect(self.data_receive)
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
                        #self.ser=serial.Serial(i[0],115200,timeout=60)
                        #SlaveSer=serial.Serial("/dev/ttyACM0",115200,timeout=60)
                    except Exception:
                        print("发生了什么错误qaq")
                    if MainGUI.ser.isOpen() :
                        MainGUI.ui.UartStates.setText(i[1]+"已经打开")
                        OpenSerSingal=1
                    else :
                        MainGUI.ui.UartStates.setText(i[1]+"未打开")
                        OpenSerSingal=0
        #SlaveSer.write("123456".encode('utf-8'))
    def UartRecBegin(self):
        global lock
        thread = Thread(target = MainGUI.Run)
        lock = Lock()
        thread.start()
    def Run():
        global lock
        while True:
            #lock.acquire()
            if MainGUI.ser.isOpen():
                count = MainGUI.ser.inWaiting()
                if count!=0:
                    UartStr=MainGUI.ser.read(count)
                    #MainGUI.UartPrint.UartPrintStr.emit(UartStr.decode('utf-8'))
                    MainGUI.ui.UartRec.append(UartStr.decode('iso-8859-1')) 
                else :
                    pass
                
                MainGUI.ser.flushInput()
            #lock.release()

    def SendMessage(self):
        MainGUI.ser.write(MainGUI.ui.UartSend.toPlainText().encode('utf-8'))
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