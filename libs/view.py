from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import caffe
import numpy as np
import cv2
import datetime


def cvnp2qimage(np_img):
    
    channels= len(np_img.shape)
    #3 channels image
    if channels==3:  
        rgb_frame=np_img
        height, width, bytesPerComponent = np_img.shape
        bytesPerLine = bytesPerComponent * width;
        # Convert to RGB for QImage.
        cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB, rgb_frame)
        #rgb_frame[...,2],rgb_frame[...,1],rgb_frame[...,0]=b[...,1],b[...,1],b[...,1]#,b[...,1],b[...,2]
        img=  QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return img
    #gray image
    elif channels==2:
        rgb_frame=np_img
        height, width = np_img.shape
        bytesPerLine =  width
        #rgb_frame[...]=np_img[...]
        img = QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format_Indexed8)
        return img
    
def cvnp2qimage_slow(np_img):
    #this method is slow but stable
    channels= len(np_img.shape)
    #3 channels image
    if channels==3:  
        height,width,channel= np_img.shape
        image = QImage(width, height, QImage.Format_RGB888)
        for x in xrange(width):
            for y in xrange(height):
                image.setPixel(x, y, qRgb(np_img[y,x,2],np_img[y,x,1],np_img[y,x,0]) )
        return image
        
    #gray image
    elif channels==2:
        height ,width = np_img.shape
        image = QImage(width, height, QImage.Format_RGB444)
        for x in xrange(width):
            for y in xrange(height):
                image.setPixel(x, y, qRgb(np_img[y,x],np_img[y,x],np_img[y,x]) )
        return image
        


def nps2qimages(nps):
    result=[]
    cnt=nps


def cvnp2caffe(cv_img):
    channels=len(cv_img.shape)
    if channels==3 :
        height, width ,channel=cv_img.shape
        cf_img=np.zeros( (channel,height, width)  )
        cf_img[0,...],cf_img[1,...],cf_img[2,...]=cv_img[...,0],cv_img[...,1],cv_img[...,2]
        return cf_img
    else: 
        height, width =cv_img.shape
        cf_img=np.zeros( (1,height, width)  )
        cf_img[0,...]=cv_img[...]
        return cf_img
        
        
def caffe2cvnp(cf_img):
    channels,height,width=cf_img.shape
    cv_img=np.zeros( (height,width,channels) )
     
    if channels==1:
        cv_img[ ... ]=cf_img[ ... ]
    else: 
        cv_img[ ...,0],cv_img[ ...,1],cv_img[ ...,2]==cf_img[0,... ],cf_img[1,... ],cf_img[2,... ]
    

def feats2qimages(feats): #feat shape  is always like that [64,26,55,55,] 
    channels =  feats.shape[1]
    height   =  feats.shape[2]
    width    =  feats.shape[3]
    bytesPerLine =  width
    qimage_list=[]
    for channel in range(channels):
            rgb_frame=feats[0,channel,...]
            img = QImage(rgb_frame.data, width, height, bytesPerLine, QImage.Format_Indexed8)
            qimage_list.append(img)
        
    return qimage_list


class DisplayBox(QWidget):
    def __init__(self):
        super(DisplayBox,self).__init__()
        self.resize(QSize(1000,1000 ))
        b=cv2.imread("cat.jpg",0)
        
        b_list=np.zeros( (10,8,b.shape[0],b.shape[1] ), dtype='uint8')
        for i in range(b_list.shape[1]):   
            b_list[0,i,...]=b

        
        images_list=feats2qimages(b_list)
        
        start=datetime.datetime.now()
        
        label_list=[]
        layout=QGridLayout()
        for index,feat in enumerate(images_list):
            tmp=QLabel()
            
            tmp.setPixmap( QPixmap.fromImage( feat  )  )
            label_list.append(tmp )
            layout.addWidget(tmp,0,index)

        self.setLayout(layout)
        end=datetime.datetime.now()              
        print end-start
        
        
app=QApplication(sys.argv)
win=DisplayBox()
win.show()
app.exec_()





