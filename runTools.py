import sys
sys.path.append("./libs")
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from btnTools import *
from functools import partial
from canvas import *
from inputDlg import *
import time
from view_dic import  *


IMG_VIEW_MODE=0
IMG_EDIT_MODE=1



class WindowMixin(object):
    
    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            addActions(menu, actions)
        return menu

 
class MainWindow(QMainWindow,WindowMixin):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)
        self.view_mode=0
        
        self.pic_view_pos=0
        self.img_list=[]
        self.img_solve_mode=IMG_EDIT_MODE
        self.statusBar()
        self.openPic_action=newAction(self, "openfile", self.openfile, "Ctrl+E", "./icons/open.png","openfile")
        self.setPoint_action=newAction(self, "setPoint", self.setPoint, "Ctrl+Q", "./icons/line.png","drawLine")
        self.drawPoint_action=newAction(self, "drawPoint", self.drawPoint, "Ctrl+W", "./icons/point.png","drawPoint")
        self.setRect_action=newAction(self, "setRect", self.setRect, "Ctrl+R", "./icons/circle.png","drawCircle")
        self.drawRect_action=newAction(self, "drawRect", self.drawRect, "Ctrl+T", "./icons/done.png","drawRect")
        
        self.nextPic_action=newAction(self, "nextPic", self.nextPic, "Ctrl+E", "./icons/next.png","nextPic")
        self.prevPic_action=newAction(self, "prevPic", self.prevPic, "Ctrl+Q", "./icons/prev.png","prevPic")
        self.viewMode_action=newAction(self, "viewMode",self.viewMode, "Ctrl+Q", "./icons/fit.png","viewMode")
        
        self.saveFile_action=newAction(self, "saveFile",self.saveFile, "Ctrl+Q", "./icons/save.png","saveFile")
        
        opentoolbar=newToolBar("tool")
        opentoolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        opentoolbar.setOrientation(Qt.Vertical)

        opentoolbar.addAction(self.openPic_action)
        opentoolbar.addAction(self.setPoint_action)
        opentoolbar.addAction(self.drawPoint_action)
        opentoolbar.addAction(self.setRect_action)
        opentoolbar.addAction(self.drawRect_action)
        opentoolbar.addAction(self.nextPic_action)
        opentoolbar.addAction(self.prevPic_action)
        opentoolbar.addAction(self.viewMode_action)
        opentoolbar.addAction(self.saveFile_action)

        self.addToolBar(Qt.LeftToolBarArea,opentoolbar)
        
    def load_last_pos(self):
        if os.path.exists("config/last_pos.txt"):
            stat=QMessageBox.information(None, "care", "do you want to back to last postion!!", QMessageBox.Yes | QMessageBox.No)
            if stat== QMessageBox.Yes:
                with open("config/last_pos.txt","r") as f:
                    print "read"
                    pos=f.read()
                    print pos
                    print "load position %s sucessfully"%pos
                    return int(pos)
            else: 
                os.remove("config/last_pos.txt")
                return 0
        else:
            return 0



    def save_last_pos(self,pos):
        with open("config/last_pos.txt","w") as f:
            f.write(str(pos))

    def openfile(self):
        self.view_mode=1
        self.update()
        filename=QFileDialog.getOpenFileName(self,"sss","./","image file (*.png *.jpg)")
        print filename
        if filename != "":
            self.canvas.loadPixmap( filename )
        
    def setPoint(self):
        if self.canvas.picfile=='':
            QMessageBox.warning(self, "warning", "please load image first!!!")
            return 
        self.point_dlg=PointDlg()
        self.point_dlg.show()
        self.point_dlg.get_point.connect( self.setPoint_slot )
        
    def setPoint_slot (self,num1,num2):
        self.canvas.setPoint( (num1, num2) )
    
    def setRect(self):
        if self.canvas.picfile=='':
            QMessageBox.warning(self, "warning", "please load image first!!!")
            return 
        self.rect_dlg=RectangleDlg()  
        self.rect_dlg.show()
        self.rect_dlg.get_rec.connect( self.setRect_slot ) 
        
    def setRect_slot (self,num1,num2,num3,num4):
        self.canvas.setRect( (num1, num2),(num3, num4) )
    
    def drawPoint(self):
        if self.canvas.picfile=='':
            QMessageBox.warning(self, "warning", "please load image first!!!")
            return 
        self.canvas.drawPoint()
        
    def drawRect(self):
        if self.canvas.picfile=='':
            QMessageBox.warning(self, "warning", "please load image first!!!")
            return 
        self.canvas.drawRect()
    
    def sizeHint(self ):
        return QSize(1000,1000)
    
    
    def keyPressEvent(self,ev):
        #ctrl+s save change to file 
        if ev.modifiers() == ( Qt.ControlModifier) and ev.key() == Qt.Key_S :
            if self.img_solve_mode==IMG_EDIT_MODE:
                if self.canvas.picfile=='':
                    QMessageBox.warning(self, "warning", "please load image first!!!")
                    return 
                else: 
                    if (self.canvas.savepoint2file("hanson")!=-1):
                        QMessageBox.warning(self, "infor", "save sucess")
            elif self.img_solve_mode==IMG_VIEW_MODE:
                canvas7points= self.canvas.get7PointsData()
                if len(self.canvas.get7PointsData().split(" ")) ==14:
                    self.viewdict.set_data(self.pic_view_pos, canvas7points)
                    QMessageBox.warning(self, "infor", "save sucess")
                else:
                    QMessageBox.warning(self, "infor", "please put 7 point")
                    
                
    def nextPic(self):
        dict_len=len(self.viewdict)
        self.pic_view_pos=(self.pic_view_pos+1) if self.pic_view_pos<dict_len-1 else dict_len-1
        self.canvas.loadPixmap( self.viewdict[self.pic_view_pos]["path"] ) 

        if self.viewdict.is_setValue(self.pic_view_pos):
            self.canvas.set7PointsData( self.viewdict.get_data(self.pic_view_pos) )
            
            if self.total_num==0:
                self.total_num-= 0 
            else:
                self.total_num-= 1 
            print self.total_num ,"left "   
        self.save_last_pos(self.pic_view_pos)
        
    def prevPic(self):
        the_last_pos=self.pic_view_pos
        self.pic_view_pos =  (self.pic_view_pos-1) if self.pic_view_pos>=1 else 0
        self.canvas.loadPixmap( self.viewdict[self.pic_view_pos]["path"] ) 
        
        if self.viewdict.is_setValue(self.pic_view_pos):
            self.canvas.set7PointsData( self.viewdict.get_data(self.pic_view_pos) )
            
            if the_last_pos==0 :
                self.total_num+= 0   
            else:
                self.total_num+= 1 

            print self.total_num  ,"left "  
            self.save_last_pos(self.pic_view_pos)    
    
    def viewMode(self):


        ret_sta=QMessageBox.information(None, "care", "do you want reset mode!!", QMessageBox.Yes | QMessageBox.No)
        if ret_sta== QMessageBox.Yes:
            self.pic_view_pos=self.load_last_pos()

            self.img_solve_mode=IMG_VIEW_MODE
            self.viewdict=ViewDict("testImageList.txt","input_rules/xy_BBox_5PointsLandmark.txt",VIEW_MODE_ALL) 
            print self.viewdict[self.pic_view_pos]["path"]
            self.canvas.loadPixmap( self.viewdict[self.pic_view_pos]["path"] ) 
            
            if self.viewdict.is_setValue(self.pic_view_pos):
                self.canvas.set7PointsData( self.viewdict.get_data(self.pic_view_pos) )

            self.total_num=len( self.viewdict  )
            print "total num :",self.total_num
        else :
            return 
        
    def saveFile(self):
        self.viewdict.save_file()
        QMessageBox.warning(self, "infor", "save sucess")
        #self.canvas.set7PointsData()
        
app=QApplication(sys.argv)
win=MainWindow()
win.show()
app.exec_()

