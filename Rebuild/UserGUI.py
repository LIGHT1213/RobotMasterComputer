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
        
class MainGUI(QObject):
    SerialRec_Singal = pyqtSignal(object)
    RgbView_Singal = pyqtSignal(object)
    GrayView_Sinagl = pyqtSignal(object)
    BinariView_Singal = pyqtSignal(object)
    CounterView_Singal = pyqtSignal(object)

    #GrayProcess_singal = pyqtSignal(object,object)
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
        #MainGUI.ui.OpenCamera.clicked.connect(MainGUI.OpenCameraProcess)
        MainGUI.ui.rgbButton.clicked.connect(MainGUI.showRGB)
        MainGUI.ui.grayButton.clicked.connect(MainGUI.showGray)
        MainGUI.ui.BinariButton.clicked.connect(MainGUI.showBinari)
        MainGUI.ui.countButton.clicked.connect(MainGUI.showCounter)

        MainGUI.UartRecBegin(self)
        MainGUI.OpenCameraProcess(self)

        self.SerialRec_Singal.connect(self.UartPrintGUI)

        self.RgbView_Singal.connect(self.showRGBPicture)
        self.GrayView_Sinagl.connect(self.showGrayPicture)
        self.BinariView_Singal.connect(self.showBinariPicture)
        self.CounterView_Singal.connect(self.showCountourPicture)

        #self.GrayProcess_singal.connect(self.ImageFindContour)
    def showRGBPicture(self,pix):
        tempIndex=MainGUI.ui.PiturestackedWidget.currentIndex()
        if tempIndex == 0:
            MainGUI.ui.rgbPicture.setPixmap(pix)
    def showGrayPicture(self,pix):
        tempIndex = MainGUI.ui.PiturestackedWidget.currentIndex()
        if tempIndex == 1:
            MainGUI.ui.grayPicture.setPixmap(pix)
    def showBinariPicture(self,pix):
        tempIndex = MainGUI.ui.PiturestackedWidget.currentIndex()
        if tempIndex == 2:
            MainGUI.ui.binarizaPicture.setPixmap(pix)
    def showCountourPicture(self,pix):
        tempIndex = MainGUI.ui.PiturestackedWidget.currentIndex()
        if tempIndex == 3:
            MainGUI.ui.CountourPicture.setPixmap(pix)
    def showRGB(self):
        MainGUI.ui.PiturestackedWidget.setCurrentIndex(0)

    def showGray(self):
        MainGUI.ui.PiturestackedWidget.setCurrentIndex(1)

    def showBinari(self):
        MainGUI.ui.PiturestackedWidget.setCurrentIndex(2)

    def showCounter(self):
        MainGUI.ui.PiturestackedWidget.setCurrentIndex(3)

    def OpenCameraProcess(self):
        global CapPicture1,ImageLock
        ImageLock=Lock()
        MainGUI.cap=cv2.VideoCapture(0)
        MainGUI.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)#设置图像宽度
        MainGUI.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)#设置图像高度
        GuiThread = Thread(target=MainGUI.UpdateImageShowThread, args=(self,))
        FindContourThread = Thread(target=MainGUI.ImageFindContour, args=(self,))
        FindContourThread.start()
        GuiThread.start()

    def UpdateImageShowThread(self):
        global CapPicture1,CapPicture2,GrayCapFlag
        while True:
            RgbRet,MainGUI.Rgbflame=MainGUI.cap.read()
            GrayRet,MainGUI.Grayflame=MainGUI.cap.read()
            if RgbRet :
                ImageLock.acquire()
                RgbCurFlame = cv2.cvtColor(MainGUI.Rgbflame, cv2.COLOR_BGR2RGB)
                CapPicture2=RgbCurFlame
                heigt, width = RgbCurFlame.shape[:2]
                RgbPic = QImage(RgbCurFlame, width, heigt, QImage.Format_RGB888)
                RgbPic = QPixmap.fromImage(RgbPic)
                #MainGUI.showPicture(self,RgbPic)
                #RgbGUI.ui.RgbView.setPixmap(RgbPic)
                self.RgbView_Singal.emit(RgbPic)
                ImageLock.release()
                #原始显示
            if GrayRet:
                ImageLock.acquire()
                MainGUI.GrayCurFlame=cv2.cvtColor(MainGUI.Grayflame,cv2.COLOR_BGR2GRAY)
                CapPicture1=MainGUI.GrayCurFlame
            #if self.RgbGUI.ui.GrayShowEnable.isChecked():
                GrayFlame=cv2.cvtColor(MainGUI.GrayCurFlame,cv2.COLOR_GRAY2RGB)
                heigt, width = GrayFlame.shape[:2]
                GrayPic = QImage(GrayFlame, width, heigt, QImage.Format_RGB888)
                GrayPic = QPixmap.fromImage(GrayPic)
                #self.RgbGUI.ui.GrayView.setPixmap(GrayPic)
                self.GrayView_Sinagl.emit(GrayPic)
                GrayCapFlag=1
                ImageLock.release()
            time.sleep(0.03)

    def ImageFindContour(self):
        global CapPicture1,CapPicture2,GrayCapFlag
        while True:
            ImageLock.acquire()
            if GrayCapFlag== 1:
                #thresh = cv2.adaptiveThreshold(CapPicture1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,5)
                blur = cv2.GaussianBlur(CapPicture1, (5, 5), 0)
                ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                image ,contor,hes= cv2.findContours ( thresh , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
                characteristicValue.Conter=contor
                characteristicValue.findMaxAreaContor(self)
                characteristicValue.findMaxLengthContor(self)
                if 1 :
                    ThreshShow = QImage(thresh.data,thresh.shape[1],thresh.shape[0],QImage.Format_Grayscale8)
                    #self.ProcessShow.ui.Binarization.setPixmap(QPixmap.fromImage(ThreshShow))
                    self.BinariView_Singal.emit(QPixmap.fromImage(ThreshShow))
                    cv2.drawContours(CapPicture2, contor, -1, (255, 0, 0), 1)
                    GrayCount = QImage(CapPicture2, CapPicture2.shape[1], CapPicture2.shape[0], QImage.Format_RGB888)
                    GrayCount = QPixmap.fromImage(GrayCount)
                    #self.ProcessShow.ui.Countour.setPixmap(GrayCount)
                    self.CounterView_Singal.emit(GrayCount)
                GrayCapFlag=0
            ImageLock.release()
            time.sleep(0.01)


#    def GetPitcure(self):

    def ClearButtom(self):
        MainGUI.ui.UartRec.clear()
    def init(self):
        self.timer = QTimer()
        #接收gui处理定时器
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
        thread = Thread(target = MainGUI.Run,args=(self,))
        lock = Lock()
        thread.start()
    def Run(self):
        global lock
        global UartStr
        while True:
            lock.acquire()
            time.sleep(0.1)
            if MainGUI.ser.isOpen():
                count = MainGUI.ser.inWaiting()
                if count!=0:
                    UartStr=MainGUI.ser.read(count)
                    UartStr=UartStr.decode('iso-8859-1')
                    #RecFlag=1
                    self.SerialRec_Singal.emit(str(UartStr))
                    #MainGUI.UartPrint.UartPrintStr.emit(UartStr)
                    #MainGUI.ui.UartRec.append(UartStr) 
                    MainGUI.ser.flushInput()
                else :
                    pass
                
                
            lock.release()

    def SendMessage(self):
        MainGUI.ser.write(MainGUI.ui.UartSend.toPlainText().encode('utf-8'))

class characteristicValue:
    ConterArea=[]
    ConterLength=[]
    MaxArea=-1
    def findMaxAreaContor(self):
        for i in range(len(characteristicValue.Conter)):
            characteristicValue.ConterArea.append(cv2.contourArea(characteristicValue.Conter[i]))
        characteristicValue.MaxArea=max(characteristicValue.ConterArea)  #注意这里我的amd处理器没有支持支持numpy的相关指令集，改在树莓派上运行时请改为numpy
        MainGUI.ui.ContorArea.setText(str(characteristicValue.MaxArea))
    def findMaxLengthContor(self):
        for i in range(len(characteristicValue.Conter)):
            characteristicValue.ConterLength.append(cv2.arcLength(characteristicValue.Conter[i],True))
        characteristicValue.MaxLength=max(characteristicValue.ConterLength)
        MainGUI.ui.ContorLength.setText(str(characteristicValue.MaxLength))
