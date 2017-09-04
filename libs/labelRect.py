from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import math


class CrossRect(object):
    def __init__(self):
        self.rect_vec=[]
        self.cnt=0
        self.move_rect_index=0
    
    def creat_new_rect(self,x1,y1,x2,y2):
        tmp_rect={}
        tmp_rect['top_x']=x1
        tmp_rect['top_y']=y1
        tmp_rect['top_x']=x2
        tmp_rect['top_y']=y2
        tmp_rect['sta']=0
        tmp_rect['name']=0
        self.point_vec.append(tmp_rect)
        self.move_poiont_index=len(self.rect_vec)-1
        self.point_vec[self.move_rect__index]['sta']=1
        
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
        
    def find_nearest_index(self,x,y):
        length=[]
        if len( self. rect_vec)==0:
            return -1
        for point in self.point_vec:
            length.append(math.sqrt( math.pow(x-rect_vec['x'], 2)+math.pow(y-rect_vec['y'], 2) ))
        
        if min(length)<60:
            self.move_poiont_index=length.index(min(length)) 
            self.point_vec[self.move_rect_index]['sta']=1
            return self.move_rect_index
        else:
            return -1
        
    def update(self):
        for s in self.point_vec:
            s['sta']=0
    
    def move_choosed_point(self,x,y):
        self.rect_vec[self.move_rect_index]['x']=x
        self.rect_vec[self.move_rect_index]['y']=y
        
            
      



    