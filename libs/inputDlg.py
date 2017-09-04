from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


class PointDlg(QDialog):
    get_point=pyqtSignal(int,int)
    
    def __init__(self,parent=None):
        super(PointDlg,self).__init__(parent)

        name=QLabel("please input label",self)
        x_lable=QLabel("x: ",self)  
        self.x_data=QLineEdit(self)
        y_label=QLabel("y: ",self)  
        self.y_data=QLineEdit(self)
        ok_btn=QPushButton("ok",self)
        cancel_btn=QPushButton("cancel",self)
        
        name.move(0,0)
        x_lable.move(0,40)
        self.x_data.move(40,40)
        y_label.move(0,80)
        self.y_data.move(40,80)
        ok_btn.move(0,120)
        cancel_btn.move(140,120)
        
        ok_btn.clicked.connect( self.ok_btn_down )
        cancel_btn.clicked.connect( self.close )
        #self.get_point.connect(self.print_test )
        
    def ok_btn_down(self):
        self.get_point.emit(int(self.x_data.text() ),int( self.y_data.text() ) )   
        self.close()
    
    def print_test(self,num1,num2):
        print "rtest",num1,num2
        
    def sizeHint(self ):
        return QSize(300,300)
    
class RectangleDlg(QDialog):
    get_rec=pyqtSignal(int,int,int,int)
    
    def __init__(self,parent=None):
        super(RectangleDlg,self).__init__(parent)

        name=QLabel("please input label",self)
        x_lable=QLabel("x: ",self)  
        self.x_data=QLineEdit(self)
        y_label=QLabel("y: ",self)  
        self.y_data=QLineEdit(self)
        w_label=QLabel("w: ",self)  
        self.w_data=QLineEdit(self)
        h_label=QLabel("h: ",self)  
        self.h_data=QLineEdit(self)
        
        ok_btn=QPushButton("ok",self)
        cancel_btn=QPushButton("cancel",self)
        
        name.move(0,0)
        x_lable.move(0,40)
        self.x_data.move(40,40)
        y_label.move(0,80)
        self.y_data.move(40,80)
        
        w_label.move(0,120)
        self.w_data.move(40,120)
        
        h_label.move(0,160)
        self.h_data.move(40,160)
        
        ok_btn.move(0,200)
        cancel_btn.move(140,200)
        
       
        ok_btn.clicked.connect( self.ok_btn_down )
        cancel_btn.clicked.connect( self.close )
        #self.get_rec.connect(self.print_test )
        
    def ok_btn_down(self):
        self.get_rec.emit(int(self.x_data.text()),int(self.y_data.text()),int(self.w_data.text()),int(self.h_data.text()) )
        self.close()   
    
    def print_test(self,num1,num2,num3,num4):
        print "rtest",num1,num2,num3,num4
        
    def sizeHint(self ):
        return QSize(300,300)
    
'''  
app=QApplication(sys.argv)
main =PointDlg()
main.show()
app.exec_()
'''
