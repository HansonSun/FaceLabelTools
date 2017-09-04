from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import math
import canvas

SHAPE_RECTANGLE =1
SHAPE_POINT=0

STATUS_NO_SELECTED=0
STATUS_SELECTED=1

class CrossPoint(object):
    def __init__(self):
        self.point_vec=[]
        self.cnt=0
        self.move_poiont_index=0
        
        self.l_space=0
        self.t_space=0
        self.b_space=0
        self.r_space=0
    
    def creat_new_point(self,p_xy):   #poin change with mouse 
        tmp_point={}
        tmp_point['x']=p_xy[0]
        tmp_point['y']=p_xy[1]
        tmp_point['shape']=SHAPE_POINT
        tmp_point['status']=STATUS_SELECTED
        tmp_point['name']=''
        self.point_vec.append(tmp_point)
        self.move_poiont_index=len(self.point_vec)-1
        
        
    def creat_new_rect(self,p_xy):   #rect change with mouse 
        tmp_point1={}
        tmp_point1['x']=p_xy[0]
        tmp_point1['y']=p_xy[1]
        tmp_point1['shape']=SHAPE_RECTANGLE
        tmp_point1['status']=STATUS_SELECTED
        tmp_point1['name']=''
        tmp_point1['new']=1
                
        tmp_point2={}
        tmp_point2['x']=p_xy[0]+100   
        tmp_point2['y']=p_xy[1]+100
        tmp_point2['shape']=SHAPE_RECTANGLE
        tmp_point2['status']=STATUS_SELECTED
        tmp_point2['name']=''
        self.point_vec.append(tmp_point1)
        self.point_vec.append(tmp_point2)
        self.move_poiont_index=len(self.point_vec)-2
        
    def put_new_point(self,p_xy):    #point are fixed
        tmp_point={}
        tmp_point['x']=p_xy[0]
        tmp_point['y']=p_xy[1]
        tmp_point['shape']=SHAPE_POINT
        tmp_point['status']=STATUS_NO_SELECTED
        tmp_point['name']=''
        self.point_vec.append(tmp_point)

        
    def put_new_rect(self,p_xy1,p_xy2): #rect are fixed
        tmp_point1={}
        tmp_point1['x']=p_xy1[0]
        tmp_point1['y']=p_xy1[1]
        tmp_point1['shape']=SHAPE_RECTANGLE
        tmp_point1['status']=STATUS_NO_SELECTED
        tmp_point1['name']=''
        tmp_point1['new']=0
        
        tmp_point2={}
        tmp_point2['x']=p_xy2[0]
        tmp_point2['y']=p_xy2[1]
        tmp_point2['shape']=SHAPE_RECTANGLE
        tmp_point2['status']=STATUS_NO_SELECTED
        tmp_point2['name']=''
        self.point_vec.append(tmp_point1)
        self.point_vec.append(tmp_point2)
        
    def remove_point(self):
        if( self.point_vec[self.move_poiont_index]['shape']==SHAPE_POINT ):
            del( self.point_vec[self.move_poiont_index] )
    
    def remove_rect(self):
        if( self.point_vec[self.move_poiont_index]['shape']==SHAPE_RECTANGLE ):
            del( self.point_vec[self.move_poiont_index] )
            del( self.point_vec[self.move_poiont_index] )
      
    def __iter__(self):
        return self

    def next(self): 
        if self.cnt > len( self.point_vec)-1 or len( self.point_vec)==0:
            self.cnt=0 
            raise StopIteration();
        self.cnt+=1
        return self.point_vec[self.cnt-1]

    def __len__(self):
        return len( self.point_vec)
        
    def find_nearest_point(self,p_xy):
        length=[]
        if len( self.point_vec)==0:
            return -1
        for point in self.point_vec:
            length.append(math.sqrt( math.pow(p_xy[0]-point['x'], 2)+math.pow(p_xy[1]-point['y'], 2) ))
        
        if min(length)<15/canvas.Canvas.scale:
            self.move_poiont_index=length.index(min(length)) 
            self.point_vec[self.move_poiont_index]['status']=STATUS_SELECTED
            return self.move_poiont_index
        else:
            return -1
        
        
    def find_nearest_rect(self,p_xy):
        cnt=len(self.point_vec)
        i=0
        while( i<cnt ):
            if self.point_vec[i]['shape']==SHAPE_POINT:
                i=i+1
                continue
            elif self.point_vec[i]['shape']==SHAPE_RECTANGLE:   
                if (p_xy[0]>self.point_vec[i]['x'])  and (p_xy[1]>self.point_vec[i]['y'])and (p_xy[0]<self.point_vec[i+1]['x']) and (p_xy[1]<self.point_vec[i+1]['y']):
                    self.move_poiont_index=i
                    self.point_vec[self.move_poiont_index]['status']=STATUS_SELECTED
                    self.point_vec[self.move_poiont_index+1]['status']=STATUS_SELECTED
                    return i
                else:
                    i=i+2
        return -1
                        
    def update(self):
        for s in self.point_vec:
            s['status']=STATUS_NO_SELECTED
        self.l_space=0
        self.t_space=0
        self.b_space=0
        self.r_space=0    
    
    
    def move_choosed_point(self,p_xy):
        self.point_vec[self.move_poiont_index]['x']=p_xy[0]
        self.point_vec[self.move_poiont_index]['y']=p_xy[1]
        
        
    def move_choosed_rect(self,p_xy):
        h=self.point_vec[self.move_poiont_index+1]['x']-self.point_vec[self.move_poiont_index]['x']
        w=self.point_vec[self.move_poiont_index+1]['y']-self.point_vec[self.move_poiont_index]['y']
        
        if self.point_vec[self.move_poiont_index]['new']==1:
            self.point_vec[self.move_poiont_index]['x']=p_xy[0]-h/2
            self.point_vec[self.move_poiont_index]['y']=p_xy[1]-w/2
            self.point_vec[self.move_poiont_index+1]['x']=p_xy[0]+h/2  
            self.point_vec[self.move_poiont_index+1]['y']=p_xy[1]+w/2
            self.point_vec[self.move_poiont_index]['new']=0
        
        else:
            if self.l_space==0 and self.t_space==0 and self.b_space==0 and self.r_space==0 :
                self.l_space=p_xy[0]-self.point_vec[self.move_poiont_index]['x']
                self.t_space=p_xy[1]-self.point_vec[self.move_poiont_index]['y']
                self.r_space=self.point_vec[self.move_poiont_index+1]['x']-p_xy[0]
                self.b_space=self.point_vec[self.move_poiont_index+1]['y']-p_xy[1]
                #print self.l_space,self.t_space,self.r_space,self.b_space
        
            self.point_vec[self.move_poiont_index]['x']=p_xy[0]-self.l_space   
            self.point_vec[self.move_poiont_index]['y']=p_xy[1]-self.t_space
            self.point_vec[self.move_poiont_index+1]['x']=p_xy[0]+self.r_space  
            self.point_vec[self.move_poiont_index+1]['y']=p_xy[1]+self.b_space 
        
    def __getitem__(self, key):
      #if key in self.point_vec:
        return self.point_vec[key]
    
    def save2file(self,img_name):
        with open("result/%s.txt"%img_name,"w+") as f:
            text=img_name+" "
            for point in self.point_vec:
                text+="%d %d "%(point["x"],point["y"])
            print text
            f.write(text[:-1])
        
    


    