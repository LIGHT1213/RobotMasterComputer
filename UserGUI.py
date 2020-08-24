import sys
from threading import Thread,Lock
import multiprocessing 
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
#不太会用python的list传参数，先用全局flag代替了
GrayCapFlag=0
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
        global CapPicture1
        RgbGUI=RgbViewGUI()
        ProcessShow=ProcessView()
        ImageLock=Lock()
        RgbGUI.ui.show()
        ProcessShow.ui.show()
        MainGUI.cap=cv2.VideoCapture(0)
        MainGUI.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)#设置图像宽度
        MainGUI.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)#设置图像高度
        def UpdateImageShowThread():
            global CapPicture1,CapPicture2,GrayCapFlag
            while True:
                
                RgbRet,MainGUI.Rgbflame=MainGUI.cap.read()
                GrayRet,MainGUI.Grayflame=MainGUI.cap.read()
                if RgbRet :
                    ImageLock.acquire()
                    CapPicture2=MainGUI.Rgbflame
                    RgbCurFlame = cv2.cvtColor(MainGUI.Rgbflame, cv2.COLOR_BGR2RGB)
                    heigt, width = RgbCurFlame.shape[:2]
                    RgbPic = QImage(RgbCurFlame, width, heigt, QImage.Format_RGB888)
                    RgbPic = QPixmap.fromImage(RgbPic)
                    RgbGUI.ui.RgbView.setPixmap(RgbPic)
                    ImageLock.release()
                    #原始显示
                if GrayRet:
                    ImageLock.acquire()
                    if GrayCapFlag==0:
                        MainGUI.GrayCurFlame=cv2.cvtColor(MainGUI.Grayflame,cv2.COLOR_BGR2GRAY)
                        CapPicture1=MainGUI.GrayCurFlame
                        GrayCapFlag=1
                    if RgbGUI.ui.GrayShowEnable.isChecked():
                        GrayFlame=cv2.cvtColor(MainGUI.GrayCurFlame,cv2.COLOR_GRAY2RGB)
                        heigt, width = GrayFlame.shape[:2]
                        GrayPic = QImage(GrayFlame, width, heigt, QImage.Format_RGB888)
                        GrayPic = QPixmap.fromImage(GrayPic)
                        RgbGUI.ui.GrayView.setPixmap(GrayPic)
                    ImageLock.release()
                time.sleep(0.03)
                
        def ImageFindContour():
            global GrayCapFlag,CapPicture1,CapPicture2
            
            
            while True:
                if GrayCapFlag==1:
                    #ImageLock.acquire()
                    #thresh = cv2.adaptiveThreshold(CapPicture1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,5)
                    blur = cv2.GaussianBlur(CapPicture1, (5, 5), 0)
                    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    ThreshShow = QImage(thresh.data,thresh.shape[1],thresh.shape[0],QImage.Format_Grayscale8)
                    ProcessShow.ui.Binarization.setPixmap(QPixmap.fromImage(ThreshShow))
                    #RgbGUI.ui.GrayView.setPixmap(QPixmap.fromImage(ThreshShow))

                    
                    image ,contor,hes= cv2.findContours ( thresh , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
                    #h=image[0]
                    cv2.drawContours(CapPicture2, contor, -1, (0, 0, 255), 3)
                    #cv2.putText(CapPicture2, "{:.3f}".format(len ( contours )), (30, 30),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 1)
                    
                    GrayCount = QImage(CapPicture2, CapPicture2.shape[1], CapPicture2.shape[0], QImage.Format_RGB888)
                    GrayCount = QPixmap.fromImage(GrayCount)
                    ProcessShow.ui.Countour.setPixmap(GrayCount)
                    #RgbGUI.ui.GrayView.setPixmap(GrayCount)
                    GrayCapFlag=0
                    #ImageLock.release()
                time.sleep(0.01)
        GuiThread = Thread(target = UpdateImageShowThread)
        FindContourThread=Thread(target=ImageFindContour)
        FindContourThread.start()
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
class RgbViewGUI:
     def __init__(self):
        RgbViewGUI.ui = uic.loadUi("UserUI/RgbView.ui")
class ProcessView:
    def __init__(self):
        ProcessView.ui= uic.loadUi("UserUI/GrayView.ui")
