import cv2
class GrayImageProcess:
    def ImageFindContour(GrayImage,lock,self):
        lock.acquire()
        thresh = cv2.adaptiveThreshold(GrayImage,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,5)
        GuiMember.image , GuiMember.contours , GuiMember.hierarchy = cv2.findContours ( binary , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE )
        lock.release()
