import sys
from threading import Thread,Lock
import time
# 系统包
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage,QPixmap
# pyqt5 部分
import serial
import serial.tools.list_ports
# 串口部分
import cv2
# opencv部分
OpenSerSingal=0
UartStr=""
RecFlag=0
CapPicture1=""
CapPicture2=""
#全局变量
def GetPitcureNum(PictureNum):
    if PictureNum==1:
        return CapPicture1
    elif PictureNum==2:
        return CapPicture2
    else:
        pass
        
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
        MainGUI.ui.OpenCamera.clicked.connect(MainGUI.OpenCameraProcess)
    def OpenCameraProcess(self):
        MainGUI.cap=cv2.VideoCapture(0)
        MainGUI.cap.set(cv2.CAP_PROP_FRAME_WIDTH,241)#设置图像宽度
        MainGUI.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,181)#设置图像高度
        def UpdateImageShowThread():
            while True:
                ret,flame=MainGUI.cap.read()
                if ret :
                    CurFlame = cv2.cvtColor(flame, cv2.COLOR_BGR2RGB)
                    heigt, width = CurFlame.shape[:2]
                    pixmap = QImage(CurFlame, width, heigt, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(pixmap)
                    MainGUI.ui.RgbLabel.setPixmap(pixmap)
        GuiThread = Thread(target = UpdateImageShowThread)
        GuiThread.start()

#    def GetPitcure(self):

    def ClearButtom(self):
        MainGUI.ui.UartRec.clear()
    def init(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.ReFlashRec)
        self.timer.start(100)
        #接收gui处理定时器
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