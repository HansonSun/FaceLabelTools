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
from ruleWidget import *
import init
from facedetect_lib import  facetool

IMG_VIEW_MODE=0
IMG_EDIT_MODE=1



 
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.view_mode=0
        self.img_list=[]
        self.img_solve_mode=IMG_EDIT_MODE

        self.initUI()

    def initUI(self):

        #init the canvas 
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        #init the toolbar
        self.statusBar()
        self.openPic_action  =newAction(self, "openfile", self.openfile, "Ctrl+E", "./icons/open.png",   "openfile"  )
        self.setPoint_action =newAction(self, "setPoint", self.setPoint, "Ctrl+Q", "./icons/line.png",   "drawLine"  )
        self.drawPoint_action=newAction(self, "drawPoint",self.drawPoint,"Ctrl+W", "./icons/point.png",  "drawPoint" )
        self.setRect_action  =newAction(self, "setRect",  self.setRect,  "Ctrl+R", "./icons/circle.png", "drawCircle")
        self.drawRect_action =newAction(self, "drawRect", self.drawRect, "Ctrl+T", "./icons/done.png",   "drawRect"  )
        self.viewMode_action =newAction(self, "viewMode", self.viewMode, "Ctrl+Q", "./icons/fit.png",    "viewMode"  )
        self.nextPic_action  =newAction(self, "nextPic",  self.nextPic,  "Ctrl+E", "./icons/next.png",   "nextPic"   )
        self.prevPic_action  =newAction(self, "prevPic",  self.prevPic,  "Ctrl+Q", "./icons/prev.png",   "prevPic"   )
        self.saveFile_action =newAction(self, "saveFile", self.saveFile, "Ctrl+Q", "./icons/save.png",   "saveFile"  )
        
        opentoolbar=newToolBar("tool")
        opentoolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        opentoolbar.setOrientation(Qt.Vertical)

        action_list=[(self.openPic_action)\
        ,(self.setPoint_action)\
        ,(self.drawPoint_action)\
        ,(self.setRect_action)\
        ,(self.drawRect_action)\
        ,(self.viewMode_action)\
        ,(self.nextPic_action)\
        ,(self.prevPic_action)\
        ,(self.saveFile_action)]


        self.add_actios_list(opentoolbar,action_list)

        self.addToolBar(Qt.LeftToolBarArea,opentoolbar)

        self.nextPic_action.setEnabled(0)
        self.prevPic_action.setEnabled(0)
        self.saveFile_action.setEnabled(0)
        self.drawRect_action.setEnabled(0)
        self.drawPoint_action.setEnabled(0)
        self.setRect_action.setEnabled(0)
        self.setPoint_action.setEnabled(0)

        
        clear_list_action=newAction(self, "generate", self.Generate_clear_list, "Ctrl+Q", "./icons/save.png",   "generate clear label file"  )

        menubar=self.menuBar()
        test_menuar  = menubar.addMenu("generate")
        test_menuar.addAction(clear_list_action)

        #test_menuar.trigger.connect(self.Generate_clear_list)
        #dock3=ruleWidget(self)  
        #dock3.setFeatures(QDockWidget.AllDockWidgetFeatures)   
        #self.addDockWidget(Qt.BottomDockWidgetArea,dock3) 
        #dock3.setVisible(0)

    def load_last_pos(self):
        if os.path.exists("./result/tmp/~last_pos.txt"):
            stat=QMessageBox.information(None, "care", "do you want to back to last postion!!", QMessageBox.Yes | QMessageBox.No)
            if stat== QMessageBox.Yes:
                with open("./result/tmp/~last_pos.txt","r") as f:
                    print "read"
                    pos=f.read()
                    print pos
                    print "load position %s sucessfully"%pos
                    return int(pos)
            else: 
                os.remove("./result/tmp/~last_pos.txt")
                return 0
        else:
            return 0

    def add_actios_list(self,thetoolbar,action_list):
        for action in action_list:
            thetoolbar.addAction(action)

    def save_last_pos(self,pos):
        with open("./result/tmp/~last_pos.txt","w") as f:
            f.write(str(pos))

    def openfile(self):
        self.openPic_action.setEnabled(0)
        self.nextPic_action.setEnabled(0)
        self.prevPic_action.setEnabled(0)
        self.saveFile_action.setEnabled(1)

        self.drawRect_action.setEnabled(1)
        self.drawPoint_action.setEnabled(1)
        self.setRect_action.setEnabled(1)
        self.setPoint_action.setEnabled(1)
        self.viewMode_action.setEnabled(0)

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

                if len(canvas7points) ==6:
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
        self.openPic_action.setEnabled(0)
        self.nextPic_action.setEnabled(1)
        self.prevPic_action.setEnabled(1)
        self.saveFile_action.setEnabled(1)

        ruledlg=ruleWidget()
        ruledlg.show()
        ruledlg.exec_()

        if init.save_change==1:
            init.save_change=0
            self.pic_view_pos=self.load_last_pos()

            self.img_solve_mode=IMG_VIEW_MODE

            self.viewdict=ViewDict(VIEW_MODE_ALL) 
            print self.viewdict[self.pic_view_pos]["path"]
            self.canvas.loadPixmap( self.viewdict[self.pic_view_pos]["path"] ) 
            
            if self.viewdict.is_setValue(self.pic_view_pos):
                self.canvas.set7PointsData( self.viewdict.get_data(self.pic_view_pos) )

            self.total_num=len( self.viewdict  )
            print "total num :",self.total_num
        else :
            return 
        
    def saveFile(self):
        self.viewdict.save_file( )
        QMessageBox.warning(self, "infor", "save sucess")
        #self.canvas.set7PointsData()
    
    def Generate_clear_list(self):
        with open("result/empty_label_file/output.txt","a") as f:
            absdirname=QFileDialog.getExistingDirectory(self,"choose directory","./")
            absdirname=str(absdirname)
            absdirname=absdirname.strip()
            dirname=absdirname.split("/")[-1]
            print dirname

            for root,subdir,files in os.walk(absdirname):
                for img_file in files:
                    tmp_dir=root[root.find(dirname):]
                    f.write("%s -1\n"%(os.path.join(tmp_dir,img_file) ))
            QMessageBox.information(self,"status","Generate sucess")
                    #print tmp_dir
                    #print os.path.join(tmp_dir,img_file)

        #detector=facetool()
        #print detector.findFaces("Aaron_Eckhart_0001.jpg",0)
        #print detector.getAbs5pFromImg("Aaron_Eckhart_0001.jpg")


app=QApplication(sys.argv)
win=MainWindow()
win.show()
app.exec_()

