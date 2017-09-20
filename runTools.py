import sys
sys.path.append("./libs")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from btnTools import *
from functools import partial
from canvas import *
from inputDlg import *
import time
from PictureViewer import  *
from RuleDialog import *
import init
from facedetect_lib import  facetool
from GenerateLabelFile import *
from TipWidget import *
from collections import OrderedDict

 
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        
        self.view_mode=0
        self.initUI()

    def initUI(self):

        #init the canvas 
        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        #init the toolbar
        self.statusBar()

        #define action
        self.openPic_action  =newAction(self, "openfile", self.openfile, "Ctrl+E", "./icons/open.png",   "openfile"  )
        self.setPoint_action =newAction(self, "setPoint", self.setPoint, "Ctrl+Q", "./icons/line.png",   "drawLine"  )
        self.drawPoint_action=newAction(self, "drawPoint",self.drawPoint,"Ctrl+W", "./icons/point.png",  "drawPoint" )
        self.setRect_action  =newAction(self, "setRect",  self.setRect,  "Ctrl+R", "./icons/circle.png", "drawCircle")
        self.drawRect_action =newAction(self, "drawRect", self.drawRect, "Ctrl+T", "./icons/done.png",   "drawRect"  )
        self.viewMode_action =newAction(self, "viewfile", self.viewFile, "Ctrl+Q", "./icons/fit.png",    "viewfile"  )
        self.nextPic_action  =newAction(self, "nextPic",  self.nextPic,  "Ctrl+E", "./icons/next.png",   "nextPic"   )
        self.prevPic_action  =newAction(self, "prevPic",  self.prevPic,  "Ctrl+Q", "./icons/prev.png",   "prevPic"   )
        self.saveFile_action =newAction(self, "saveFile", self.saveFile, "Ctrl+Q", "./icons/save.png",   "saveFile"  )
        self.default_point_action=newAction(self, "default", self.put_default_7point, "Ctrl+D", "./icons/default.png",   "default"  )

        clear_list_action=newAction(self, "generate", self.Generate_clear_labelfile, "Ctrl+Q", "./icons/save.png",   "generate clear label file"  )
        labeled_list_action=newAction(self, "generate", self.Generate_labeled_labelfile, "Ctrl+Q", "./icons/save.png",   "generate clear label file"  )

        filetoolbar=newToolBar("tool")
        filetoolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        edittoolbar=newToolBar("edit")
        edittoolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        #add action to toolbar
        action_list=[(self.openPic_action)\
        ,(self.viewMode_action)\
        ,(self.nextPic_action)\
        ,(self.prevPic_action)\
        ,(self.saveFile_action)]

        self.add_actios_list(filetoolbar,action_list)

        action_list=[(self.setPoint_action)\
        ,(self.drawPoint_action)\
        ,(self.setRect_action)\
        ,(self.drawRect_action)\
        ,(self.default_point_action)]

        self.add_actios_list(edittoolbar,action_list)


        self.addToolBar(Qt.TopToolBarArea,filetoolbar)
        self.addToolBar(Qt.LeftToolBarArea,edittoolbar)

        #enable and disable some button
        self.nextPic_action.setEnabled(0)
        self.prevPic_action.setEnabled(0)
        self.saveFile_action.setEnabled(0)
        self.drawRect_action.setEnabled(0)
        self.drawPoint_action.setEnabled(0)
        self.setRect_action.setEnabled(0)
        self.setPoint_action.setEnabled(0)
        self.default_point_action.setEnabled(0)

        

        tool_menubar=self.menuBar()
        tool_menubar_1  = tool_menubar.addMenu("generate clear list")
        tool_menubar_1.addAction(clear_list_action)

        test_menuar_2  = tool_menubar.addMenu("generate labeled list")
        test_menuar_2.addAction(labeled_list_action)


        self.tipwidget=TipWidget()
        self.tipwidget.setFeatures(QDockWidget.AllDockWidgetFeatures)   
        self.addDockWidget(Qt.RightDockWidgetArea,self.tipwidget) 


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
        ruledlg=RuleDialog(1)
        ruledlg.show()
        ruledlg.exec_()
        
        self.pic_view_pos=0

        if init.glb_save_change==1:
            init.glb_save_change=0

            self.pictureviewer=PictureViewer(init.glb_view_mode) 
            print "open",self.pictureviewer[self.pic_view_pos]["abspath"],"sucessful"
            self.canvas.loadPixmap( self.pictureviewer[self.pic_view_pos]["abspath"] ) 
            
            if self.pictureviewer.is_empty(self.pic_view_pos):
                self.canvas.set7PointsData( self.pictureviewer.get_data(self.pic_view_pos) )

            self.nextPic_action.setEnabled(0)
            self.prevPic_action.setEnabled(0)
            self.saveFile_action.setEnabled(1)
            self.drawRect_action.setEnabled(1)
            self.drawPoint_action.setEnabled(1)
            self.setRect_action.setEnabled(1)
            self.setPoint_action.setEnabled(1)
            self.viewMode_action.setEnabled(1)
            self.default_point_action.setEnabled(1)

        else :
            return 
        
        
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

            canvas7points= self.canvas.get7PointsData()

            if init.glb_7p_warning==True:
                if len(canvas7points) ==7:
                    self.pictureviewer.set_data(self.pic_view_pos, canvas7points)
                    QMessageBox.warning(self, "infor", "save sucess")
                else:
                    QMessageBox.warning(self, "infor", "please put 7 point")
            else:
                self.pictureviewer.set_data(self.pic_view_pos, canvas7points)
                QMessageBox.warning(self, "infor", "save sucess")
                    
                
    def nextPic(self):
        dict_len=len(self.pictureviewer)

        self.pic_view_pos=(self.pic_view_pos+1) if self.pic_view_pos<dict_len-1 else dict_len-1
        self.canvas.loadPixmap( self.pictureviewer[self.pic_view_pos]["abspath"] ) 

        if not self.pictureviewer.is_empty(self.pic_view_pos):
            self.canvas.set7PointsData( self.pictureviewer.get_data(self.pic_view_pos) )
            

        print "total num:",self.total_num,"  left num:",self.total_num-self.pic_view_pos
        self.save_last_pos(self.pic_view_pos)
        
    def prevPic(self):

        self.pic_view_pos =  (self.pic_view_pos-1) if self.pic_view_pos>=1 else 0
        self.canvas.loadPixmap( self.pictureviewer[self.pic_view_pos]["abspath"] ) 
        
        if not self.pictureviewer.is_empty(self.pic_view_pos):
            self.canvas.set7PointsData( self.pictureviewer.get_data(self.pic_view_pos) )


        print "total num:",self.total_num,"   left num:",self.total_num-self.pic_view_pos
        self.save_last_pos(self.pic_view_pos)    
    
    def viewFile(self):


        ruledlg=RuleDialog(0)
        ruledlg.show()
        ruledlg.exec_()

        if init.glb_save_change==1:
            init.glb_save_change=0
            self.pic_view_pos=self.load_last_pos()

            self.pictureviewer=PictureViewer(init.glb_view_mode) 

            self.canvas.loadPixmap( self.pictureviewer[self.pic_view_pos]["abspath"] ) 

            if not self.pictureviewer.is_empty(self.pic_view_pos):
                self.canvas.set7PointsData( self.pictureviewer.get_data(self.pic_view_pos) )

            self.left_num=len( self.pictureviewer )
            self.total_num=len( self.pictureviewer )

            print "total num :",self.total_num

            self.drawRect_action.setEnabled(1)
            self.drawPoint_action.setEnabled(1)
            self.setRect_action.setEnabled(1)
            self.setPoint_action.setEnabled(1)

            self.openPic_action.setEnabled(0)
            self.nextPic_action.setEnabled(1)
            self.prevPic_action.setEnabled(1)
            self.saveFile_action.setEnabled(1)
            self.default_point_action.setEnabled(1)
        else :
            return 
        
    def saveFile(self):
        if self.pictureviewer.save_file( )==1:
            QMessageBox.warning(self, "infor", "save sucess")
    
    def Generate_labeled_labelfile(self):
        absdirname=QFileDialog.getExistingDirectory(self,"choose directory","./")
        absdirname=str(absdirname)
        absdirname=absdirname.strip()

        detector=facetool()
        self.genThread = GenerateLabelFile(detector,absdirname)
        self.genThread.start()

    def Generate_clear_labelfile(self):
       
        absdirname=QFileDialog.getExistingDirectory(self,"choose directory","./")
        absdirname=str(absdirname)
        absdirname=absdirname.strip()
        dirname=absdirname.split("/")[-1]
        print dirname

        with open("result/clear_label_file/clear_%s.txt"%dirname,"a") as f:

            for root,subdir,files in os.walk(absdirname):
                for img_file in files:
                    tmp_dir=root[root.find(dirname):]
                    f.write("%s -1\n"%(os.path.join(tmp_dir,img_file) ))
            QMessageBox.information(self,"status","Generate sucess")

 
    def put_default_7point(self):
        img=cv2.imread( self.pictureviewer[self.pic_view_pos]["abspath"],0 )
        width=img.shape[1]
        height=img.shape[0]

        distance_pw=width/10
        distance_ph=height/10

        distance_rw=width/5
        distance_rh=height/5

        mid_point=(width/2,height/2)

        data_dict=OrderedDict()
        data_dict['rect2p_1']=( (mid_point[0]-distance_rw,mid_point[1]-distance_rh),(mid_point[0]+distance_rw,mid_point[1]+distance_rh) )
        data_dict['point_1']=(mid_point[0]-distance_pw,mid_point[1]-distance_ph)
        data_dict['point_2']=(mid_point[0]+distance_pw,mid_point[1]-distance_ph)
        data_dict['point_3']=mid_point
        data_dict['point_4']=(mid_point[0]-distance_pw,mid_point[1]+distance_ph)
        data_dict['point_5']=(mid_point[0]+distance_pw,mid_point[1]+distance_ph)

        self.canvas.set7PointsData( data_dict )

app=QApplication(sys.argv)
win=MainWindow()
win.show()
app.exec_()

