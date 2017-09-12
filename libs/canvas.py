from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import math
from labelPoint import *
import init

MODE_DRAW_POINT=0
MODE_DRAW_REC=1
MODE_DRAW_CIRCLE=2


MODE_MOVE_POINT=3
MODE_MOVE_REC=4


MODE_LOAD_IMAG=5
MODE_FREE=6

start_scale=2

class Canvas(QWidget):
    scale=start_scale
    def __init__(self,parent=None):
        super(Canvas, self).__init__(parent)
        self._painter = QPainter()
        self.picfile=''
        self.pixmap=QPixmap()
        self.pic_origin_height=0
        self.pic_origin_width=0
        self.pic_scaled_height=0
        self.pic_scaled_width=0
        Canvas.scale=start_scale
        
        self.axis_move_x=0
        self.axis_move_y=0
        
        self.point_vec=CrossPoint()
        self.mode = MODE_FREE
        self.setMouseTracking(True)      
        
    def loadPixmap(self, picfile):
        self.reset()
        self.mode=MODE_LOAD_IMAG
        self.picfile = picfile
        self.pixmap=QPixmap(self.picfile)
        self.shapes = []
        self.repaint()
    
    def reset(self):
        self.picfile=''
        self.pixmap=QPixmap()
        self.pic_origin_height=0
        self.pic_origin_width=0
        self.pic_scaled_height=0
        self.pic_scaled_width=0
        Canvas.scale=start_scale
        self.axis_move_x=0
        self.axis_move_y=0
        self.point_vec=CrossPoint()
        self.mode = MODE_FREE
    
    def setPoint(self, point):
        self.point_vec.put_new_point( point )
        self.mode=MODE_FREE
           
    def setRect(self,point_1,point_2):
        self.point_vec.put_new_rect( point_1,point_2 )
        self.mode=MODE_FREE
        
    def drawPoint(self):
        self.point_vec.creat_new_point( (0 , 0) )
        self.mode=MODE_MOVE_POINT
           
    def drawRect(self):
        self.point_vec.creat_new_rect( (0 , 0) )
        self.mode=MODE_MOVE_REC

    def drawshape(self,painter,point_v):  #used to draw point and rectangle
        
        point_cnt=len(point_v)

        if point_cnt==0:
            return 
        i=0
        while(i<point_cnt):
            if point_v[i]['shape']== SHAPE_RECTANGLE: #draw rectangle
                if(point_v[i]['status']==STATUS_SELECTED or point_v[i+1]['status']==STATUS_SELECTED): #move status
                    painter.setPen(QColor(255,225,0,))
                    h=point_v[i+1]['y']-point_v[i]['y']
                    w=point_v[i+1]['x']-point_v[i]['x']
                    painter.drawText(QPoint(point_v[i]['x']+int(20/Canvas.scale),point_v[i]['y']), str(i) )
                    painter.drawText(QPoint(point_v[i+1]['x']-int(30/Canvas.scale),point_v[i+1]['y']), str(i+1) )
                    painter.drawRect(point_v[i]['x'],point_v[i]['y'],w,h)
                    painter.drawEllipse( QPoint(point_v[i]['x'],point_v[i]['y']),int(10/Canvas.scale),int(10/Canvas.scale)  )
                    painter.drawEllipse( QPoint(point_v[i+1]['x'],point_v[i+1]['y']),int(10/Canvas.scale),int(10/Canvas.scale)  )
                    i=i+2
                else: #free status
                    painter.setPen(QColor(255,0,0,))
                    h=point_v[i+1]['y']-point_v[i]['y']
                    w=point_v[i+1]['x']-point_v[i]['x']
                    painter.drawText(QPoint(point_v[i]['x']+int(20/Canvas.scale),point_v[i]['y']), str(i) )
                    painter.drawText(QPoint(point_v[i+1]['x']-int(30/Canvas.scale),point_v[i+1]['y']), str(i+1) )
                    painter.drawRect(point_v[i]['x'],point_v[i]['y'],w,h)
                    painter.drawEllipse( QPoint(point_v[i]['x'],point_v[i]['y']),int(10/Canvas.scale),int(10/Canvas.scale)  )
                    painter.drawEllipse( QPoint(point_v[i+1]['x'],point_v[i+1]['y']),int(10/Canvas.scale),int(10/Canvas.scale)  )
                    i=i+2      
                
            else:#draw point
                if( point_v[i]['status']==STATUS_SELECTED): #set pen color according to the status
                    painter.setPen(QColor(255,220,0,))
                else:
                    painter.setPen(QColor(255,0,0,))
               
                painter.drawText(QPoint(point_v[i]['x']-int(30/Canvas.scale),point_v[i]['y']), str(i) )
                painter.drawEllipse( QPoint(point_v[i]['x'],point_v[i]['y']),int(15/Canvas.scale),int(15/Canvas.scale)  )
                painter.drawLine(point_v[i]['x'],point_v[i]['y']-int(30/Canvas.scale),point_v[i]['x'],point_v[i]['y']+int(30/Canvas.scale))
                painter.drawLine(point_v[i]['x']-int(30/Canvas.scale),point_v[i]['y'],point_v[i]['x']+int(30/Canvas.scale),point_v[i]['y'])
                i=i+1     
            
    def paintEvent(self, event):
        '''
        if self.pixmap is None:
            super(Canvas, self).paintEvent(event)
        else:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing,True)
            painter.drawPixmap( self.rect(), self.pixmap )
       
        '''
        
        painter =QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        font=QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(int (18/Canvas.scale))
        font.setItalic(True)
        painter.setFont(font)
        
        
        self.pic_origin_height=self.pixmap.height()
        self.pic_origin_width=self.pixmap.width()
        self.pic_scaled_height=self.pic_origin_height*Canvas.scale
        self.pic_scaled_width=self.pic_origin_width*Canvas.scale
        
        self.axis_move_x=(self.rect().width()-self.pic_scaled_width)/2
        self.axis_move_y=(self.rect().height()-self.pic_scaled_height)/2
        
        painter.translate( int(self.axis_move_x),int(self.axis_move_y) )
        painter.scale(Canvas.scale,Canvas.scale)
        painter.drawPixmap(0,0,self.pixmap)
        
        self.drawshape(painter,self.point_vec)
            
    def mousePressEvent(self, ev):
        if self.is_inbox(ev.pos().x(),ev.pos().y() )==1  :
            if ev.button()==Qt.LeftButton:
               
                if self.mode==MODE_FREE :
                    
                    if self.point_vec.find_nearest_point(self.new_point_xy(ev.pos().x(),ev.pos().y()) )==-1:
                        if self.point_vec.find_nearest_rect( self.new_point_xy(ev.pos().x(),ev.pos().y()) )==-1:
                            return 
                        else:
                            self.mode=MODE_MOVE_REC
                    else:
                        self.mode=MODE_MOVE_POINT
                
                elif self.mode==MODE_MOVE_POINT:
                    self.point_vec.update()
                    self.mode=MODE_FREE
                    self.update()
                    
                elif self.mode==MODE_MOVE_REC:
                    self.point_vec.update()
                    self.mode=MODE_FREE
                    self.update()
                    
            elif ev.button()==Qt.RightButton:
                if self.mode==MODE_FREE :
                    if self.point_vec.find_nearest_point(self.new_point_xy(ev.pos().x(),ev.pos().y()) )==-1:
                        if self.point_vec.find_nearest_rect( self.new_point_xy(ev.pos().x(),ev.pos().y()) )==-1:
                            return 
                        else:
                            
                            #print "in rect ",self.point_vec.move_poiont_index
                            self.point_vec.remove_rect()
                    else:
                        
                        #print "in point",self.point_vec.move_poiont_index
                        self.point_vec.remove_point()
                            
    def wheelEvent(self, ev):
        if ev.orientation() == Qt.Vertical:
            mods=ev.modifiers()
            if int(mods)==Qt.ControlModifier:
                if( ev.delta() >0):
                    if(Canvas.scale<3):
                        Canvas.scale+=0.02
                else:
                    if(Canvas.scale>0.04):
                        Canvas.scale-=0.02      
                self.update()
            
    def savepoint2file(self,img_name):
        if (len(self.point_vec)==0):
             QMessageBox.warning(self, "warning", "no point detect")
             return -1
        else:
            self.point_vec.save2file(img_name) 
            return 1 
                
    def get7PointsData(self):
        text=""
        for point in self.point_vec.point_vec:
                text+="%d %d "%(point["x"],point["y"]) 
        
        return init.from_dict_to_rule(text)

    
    def set7PointsData(self,data):

        for key,value in data.items():
            if(key.find("rect2p")==0):
                self.setRect( value[0],value[1] )
            if(key.find("point")==0):
                self.setPoint( value )
        

        self.update()

    
    '''         
    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.RightButton:
            print "rr"
        else:
            print "lr"
    '''  
    def mouseMoveEvent(self, ev):
        if self.is_inbox(ev.pos().x(),ev.pos().y() )==1  :
            if self.mode==MODE_FREE:
               # print self.new_point_xy(ev.pos().x(),ev.pos().y() )
                self.update()    
            elif self.mode==MODE_MOVE_POINT:
                self.point_vec.move_choosed_point( self.new_point_xy(ev.pos().x(),ev.pos().y()) ) 
                self.update()
                #self.update(self.point_vec[0]['x']-100,self.point_vec[0]['y']-100,200,200) 
            elif self.mode==MODE_MOVE_REC:
                self.point_vec.move_choosed_rect( self.new_point_xy(ev.pos().x(),ev.pos().y()) ) 
                self.update()
                
  
    def scaled(self,num):
        return num*Canvas.scale  
    
    def new_point_x(self,x):
        if x>self.axis_move_x and x<self.axis_move_x+self.pic_scaled_width:
            return int((x-int(self.axis_move_x))/Canvas.scale)
        else:
            return -1
        
    def new_point_y(self,y):
        if y>self.axis_move_y and y<self.axis_move_y+self.pic_scaled_height:
            return int((y -int(self.axis_move_y))/Canvas.scale)
        else:
            return -1
        
    def new_point_xy(self,x,y):
        return int((x-int(self.axis_move_x))/Canvas.scale) , int((y -int(self.axis_move_y))/Canvas.scale)

    def is_inbox(self,x,y):
        if x<self.axis_move_x or x>self.axis_move_x+self.pic_scaled_width or y<self.axis_move_y or y>self.axis_move_y+self.pic_scaled_height:
            return 0
        else :
            return 1

if __name__=="__main__":
    app=QApplication(sys.argv)
    main =Canvas()
    main.show()
    app.exec_()


