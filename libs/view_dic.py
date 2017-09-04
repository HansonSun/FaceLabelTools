import os,sys
import random

VIEW_MODE_ALL=0
VIEW_MODE_UNLABELED=1
VIEW_MODE_LABELED=2
VIEW_MODE_RANDOM=3

FILETYPE_Face2Point_and_Landmark=0
FILETYPE_FaceRect_and_Landmark=1
FILETYPE_FaceBBox_and_Landmark=2
FILETYPE_Face2Point=3
FILETYPE_FaceRect=4
FILETYPE_FaceBBox=5

class Face2Point_and_Landmark (object):
    def __init__(self,infor_file,mode=VIEW_MODE_UNLABELED):
        #self.dic_item_template={"flag":0,path":"","left_top":[],"bottom_right":[],"eye_l":[0,0],"eye_r":[0,0],"nose":[0,0],"mouth_l":[0,0],"mouth_r":[0,0] }
        self.infor_list=[]
        self.view_index=[]  #used with view_mode
        self.cur_flag=0
        self.counter=0
        self.view_mode=mode
        f=open(infor_file,"r")
        
        for index,line in enumerate(f.readlines()):
            text= line.split(" ")
            dic_item_template={}
            if( int(text[1])==-1):
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=0
                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.view_index.append(index)
            else:
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=1
                dic_item_template["left_top"]=(int(float(text[1])),int(float(text[2])) )
                dic_item_template["bottom_right"]=(int(float(text[3])),int(float(text[4])) )
                dic_item_template["eye_l"]=(int(float(text[5])),int(float(text[6])) )
                dic_item_template["eye_r"]=(int(float(text[7])),int(float(text[8])) )
                dic_item_template["nose"]=(int(float(text[9])),int(float(text[10])) )
                dic_item_template["mouth_l"]=(int(float(text[11])),int(float(text[12])) )
                dic_item_template["mouth_r"]=(int(float(text[13])),int(float(text[14])) )
                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.view_index.append(index)
                    
            self.infor_list.append(dic_item_template)
            
        if  self.view_mode==VIEW_MODE_RANDOM:
            self.view_index=random.sample(self.view_index,1000)
      
    def read(self):
        pass
    
    def set_data(self,key,data):
        data=data.split(" ")
        index=self.view_index[key]
        self.infor_list[index]["flag"]=1
        self.infor_list[index]["left_top"]=( int(float(data[0])),int(float(data[1])) )
        self.infor_list[index]["bottom_right"]=( int(float(data[2])),int(float(data[3])) )
        self.infor_list[index]["eye_l"]=( int(float(data[4])),int(float(data[5])) )
        self.infor_list[index]["eye_r"]=( int(float(data[6])),int(float(data[7])) )
        self.infor_list[index]["nose"]=( int(float(data[8])),int(float(data[9])) )
        self.infor_list[index]["mouth_l"]=( int(float(data[10])),int(float(data[11])) )
        self.infor_list[index]["mouth_r"]=( int(float(data[12])),int(float(data[13])) )
    
    def get_data(self,key):
        item=self.infor_list[self.view_index[key]]
        output="%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
        return output
    
    
    def is_setValue(self,key):
        return self.infor_list[self.view_index[key]]["flag"]
    
    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.infor_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
            else:
                output="%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["path"],item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
            f.write( output )
        f.close() 
    
    def disply(self):
        for item in self.view_index:
            print self.infor_list[item]

        
    def __getitem__(self, key):
        return self.infor_list[self.view_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.view_index)-1 or len( self.view_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.infor_list[self.view_index[self.counter-1]]
    
    def __len__(self):
        return len(self.view_index)
    

class FaceRect_and_Landmark (object):
    def __init__(self,infor_file,mode=VIEW_MODE_UNLABELED):
        #self.dic_item_template={"flag":0,path":"","left_top":[],"bottom_right":[],"eye_l":[0,0],"eye_r":[0,0],"nose":[0,0],"mouth_l":[0,0],"mouth_r":[0,0] }
        self.infor_list=[]
        self.view_index=[]  #used with view_mode
        self.cur_flag=0
        self.counter=0
        self.view_mode=mode
        f=open(infor_file,"r")
        
        for index,line in enumerate(f.readlines()):
            text= line.split(" ")
            dic_item_template={}
            if( int(text[1])==-1):
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=0
                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.view_index.append(index)
            else:
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=1
                dic_item_template["left_top"]=( int(text[1]),int(text[2]) ) 
                dic_item_template["bottom_right"]=( int(text[1])+int(text[3]), int(text[2])+int(text[4]) )
                dic_item_template["eye_l"]=(int(text[5]),int(text[6]) )
                dic_item_template["eye_r"]=(int(text[7]),int(text[8]) )
                dic_item_template["nose"]=(int(text[9]),int(text[10]) )
                dic_item_template["mouth_l"]=(int(text[11]),int(text[12]) )
                dic_item_template["mouth_r"]=(int(text[13]),int(text[14]) )
                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.view_index.append(index)
                    
            self.infor_list.append(dic_item_template)
            
        if  self.view_mode==VIEW_MODE_RANDOM:
            self.view_index=random.sample(self.view_index,1000)
      
    def read(self):
        pass
    
    def set_data(self,key,data):
        data=data.split(" ")
        index=self.view_index[key]
        self.infor_list[index]["flag"]=1
        self.infor_list[index]["left_top"]=(int(data[0]),int(data[1]) )
        self.infor_list[index]["bottom_right"]=(int(data[2]),int(data[3]) )
        self.infor_list[index]["eye_l"]=(int(data[4]),int(data[5]) )
        self.infor_list[index]["eye_r"]=(int(data[6]),int(data[7]) )
        self.infor_list[index]["nose"]=(int(data[8]),int(data[9]) )
        self.infor_list[index]["mouth_l"]=(int(data[10]),int(data[11]) )
        self.infor_list[index]["mouth_r"]=(int(data[12]),int(data[13]) )
    
    def get_data(self,key):
        item=self.infor_list[self.view_index[key]]
        output="%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
        return output
    
    
    def is_setValue(self,key):
        return self.infor_list[self.view_index[key]]["flag"]
    
    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.infor_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
            else:
                output="%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["path"],item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
            f.write( output )
        f.close() 
    
    def disply(self):
        for item in self.view_index:
            print self.infor_list[item]

        
    def __getitem__(self, key):
        return self.infor_list[self.view_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.view_index)-1 or len( self.view_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.infor_list[self.view_index[self.counter-1]]
    
    def __len__(self):
        return len(self.view_index)


class FaceBBox_and_Landmark (object):
    def __init__(self,infor_file,mode=VIEW_MODE_UNLABELED):
        self.infor_list=[]
        self.view_index=[]  #used with view_mode
        self.cur_flag=0
        self.counter=0
        self.view_mode=mode
        f=open(infor_file,"r")
        
        for index,line in enumerate(f.readlines()):
            text= line.split(" ")
            dic_item_template={}
            if( int(text[1])==-1):
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=0
                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.view_index.append(index)
            else:
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=1
                dic_item_template["left_top"]=(int(float(text[1])),int(float(text[3])) )
                dic_item_template["bottom_right"]=(int(float(text[2])),int(float(text[4])) )
                dic_item_template["eye_l"]=(int(float(text[5])),int(float(text[6])) )
                dic_item_template["eye_r"]=(int(float(text[7])),int(float(text[8])) )
                dic_item_template["nose"]=(int(float(text[9])),int(float(text[10])) )
                dic_item_template["mouth_l"]=(int(float(text[11])),int(float(text[12])) )
                dic_item_template["mouth_r"]=(int(float(text[13])),int(float(text[14])) )
                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.view_index.append(index)
                    
            self.infor_list.append(dic_item_template)
            
        if  self.view_mode==VIEW_MODE_RANDOM:
            self.view_index=random.sample(self.view_index,1000)
      
    def read(self):
        pass
    
    def set_data(self,key,data):
        data=data.split(" ")
        index=self.view_index[key]
        self.infor_list[index]["flag"]=1
        self.infor_list[index]["left_top"]=(int(data[0]),int(data[1]) )
        self.infor_list[index]["bottom_right"]=(int(data[2]),int(data[3]) )
        self.infor_list[index]["eye_l"]=(int(data[4]),int(data[5]) )
        self.infor_list[index]["eye_r"]=(int(data[6]),int(data[7]) )
        self.infor_list[index]["nose"]=(int(data[8]),int(data[9]) )
        self.infor_list[index]["mouth_l"]=(int(data[10]),int(data[11]) )
        self.infor_list[index]["mouth_r"]=(int(data[12]),int(data[13]) )
    
    def get_data(self,key):
        item=self.infor_list[self.view_index[key]]
        output="%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
        return output
    
    
    def is_setValue(self,key):
        return self.infor_list[self.view_index[key]]["flag"]
    
    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.infor_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
            else:
                output="%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["path"],item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
            f.write( output )
        f.close() 
    
    def disply(self):
        for item in self.view_index:
            print self.infor_list[item]

        
    def __getitem__(self, key):
        return self.infor_list[self.view_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.view_index)-1 or len( self.view_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.infor_list[self.view_index[self.counter-1]]
    
    def __len__(self):
        return len(self.view_index)
   

class Face2Point (object):
    def __init__(self,infor_file,mode=VIEW_MODE_UNLABELED):
        #self.dic_item_template={"flag":0,path":"","left_top":[],"bottom_right":[],"eye_l":[0,0],"eye_r":[0,0],"nose":[0,0],"mouth_l":[0,0],"mouth_r":[0,0] }
        self.infor_list=[]
        self.view_index=[]  #used with view_mode
        self.cur_flag=0
        self.counter=0
        self.view_mode=mode
        f=open(infor_file,"r")
        
        for index,line in enumerate(f.readlines()):
            text= line.split(" ")
            dic_item_template={}
            if( int(text[1])==-1):
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=0
                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.view_index.append(index)
            else:
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=1
                dic_item_template["left_top"]=(int(float(text[1])),int(float(text[2])) )
                dic_item_template["bottom_right"]=(int(float(text[3])),int(float(text[4])) )
                dic_item_template["eye_l"]=(int(float(text[5])),int(float(text[6])) )
                dic_item_template["eye_r"]=(int(float(text[7])),int(float(text[8])) )
                dic_item_template["nose"]=(int(float(text[9])),int(floa(text[10])) )
                dic_item_template["mouth_l"]=(int(float(text[11])),int(float(text[12])) )
                dic_item_template["mouth_r"]=(int(float(text[13])),int(float(text[14])) )
                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.view_index.append(index)
                    
            self.infor_list.append(dic_item_template)
            
        if  self.view_mode==VIEW_MODE_RANDOM:
            self.view_index=random.sample(self.view_index,1000)
      
    def read(self):
        pass
    
    def set_data(self,key,data):
        data=data.split(" ")
        index=self.view_index[key]
        self.infor_list[index]["flag"]=1
        self.infor_list[index]["left_top"]=(int(data[0]),int(data[1]) )
        self.infor_list[index]["bottom_right"]=(int(data[2]),int(data[3]) )
        self.infor_list[index]["eye_l"]=(int(data[4]),int(data[5]) )
        self.infor_list[index]["eye_r"]=(int(data[6]),int(data[7]) )
        self.infor_list[index]["nose"]=(int(data[8]),int(data[9]) )
        self.infor_list[index]["mouth_l"]=(int(data[10]),int(data[11]) )
        self.infor_list[index]["mouth_r"]=(int(data[12]),int(data[13]) )
    
    def get_data(self,key):
        item=self.infor_list[self.view_index[key]]
        output="%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
        return output
    
    
    def is_setValue(self,key):
        return self.infor_list[self.view_index[key]]["flag"]
    
    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.infor_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
            else:
                output="%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["path"],item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
            f.write( output )
        f.close() 
    
    def disply(self):
        for item in self.view_index:
            print self.infor_list[item]

        
    def __getitem__(self, key):
        return self.infor_list[self.view_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.view_index)-1 or len( self.view_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.infor_list[self.view_index[self.counter-1]]
    
    def __len__(self):
        return len(self.view_index)
   

class FaceRect (object):
    def __init__(self,infor_file,mode=VIEW_MODE_UNLABELED):
        #self.dic_item_template={"flag":0,path":"","left_top":[],"bottom_right":[],"eye_l":[0,0],"eye_r":[0,0],"nose":[0,0],"mouth_l":[0,0],"mouth_r":[0,0] }
        self.infor_list=[]
        self.view_index=[]  #used with view_mode
        self.cur_flag=0
        self.counter=0
        self.view_mode=mode
        f=open(infor_file,"r")
        
        for index,line in enumerate(f.readlines()):
            text= line.split(" ")
            dic_item_template={}
            if( int(text[1])==-1):
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=0
                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.view_index.append(index)
            else:
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=1
                dic_item_template["left_top"]=(int(float(text[1])),int(float(text[2])) )
                dic_item_template["bottom_right"]=(int(float(text[3])),int(float(text[4])) )
                dic_item_template["eye_l"]=(int(float(text[5])),int(float(text[6])) )
                dic_item_template["eye_r"]=(int(float(text[7])),int(float(text[8])) )
                dic_item_template["nose"]=(int(float(text[9])),int(float(text[10])) )
                dic_item_template["mouth_l"]=(int(float(text[11])),int(float(text[12])) )
                dic_item_template["mouth_r"]=(int(float(text[13])),int(float(text[14])) )
                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.view_index.append(index)
                    
            self.infor_list.append(dic_item_template)
            
        if  self.view_mode==VIEW_MODE_RANDOM:
            self.view_index=random.sample(self.view_index,1000)
      
    def read(self):
        pass
    
    def set_data(self,key,data):
        data=data.split(" ")
        index=self.view_index[key]
        self.infor_list[index]["flag"]=1
        self.infor_list[index]["left_top"]=(int(data[0]),int(data[1]) )
        self.infor_list[index]["bottom_right"]=(int(data[2]),int(data[3]) )
        self.infor_list[index]["eye_l"]=(int(data[4]),int(data[5]) )
        self.infor_list[index]["eye_r"]=(int(data[6]),int(data[7]) )
        self.infor_list[index]["nose"]=(int(data[8]),int(data[9]) )
        self.infor_list[index]["mouth_l"]=(int(data[10]),int(data[11]) )
        self.infor_list[index]["mouth_r"]=(int(data[12]),int(data[13]) )
    
    def get_data(self,key):
        item=self.infor_list[self.view_index[key]]
        output="%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
        return output
    
    
    def is_setValue(self,key):
        return self.infor_list[self.view_index[key]]["flag"]
    
    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.infor_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
            else:
                output="%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["path"],item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
            f.write( output )
        f.close() 
    
    def disply(self):
        for item in self.view_index:
            print self.infor_list[item]

        
    def __getitem__(self, key):
        return self.infor_list[self.view_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.view_index)-1 or len( self.view_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.infor_list[self.view_index[self.counter-1]]
    
    def __len__(self):
        return len(self.view_index)
   

class FaceBBox (object):
    def __init__(self,infor_file,mode=VIEW_MODE_UNLABELED):
        #self.dic_item_template={"flag":0,path":"","left_top":[],"bottom_right":[],"eye_l":[0,0],"eye_r":[0,0],"nose":[0,0],"mouth_l":[0,0],"mouth_r":[0,0] }
        self.infor_list=[]
        self.view_index=[]  #used with view_mode
        self.cur_flag=0
        self.counter=0
        self.view_mode=mode
        f=open(infor_file,"r")
        
        for index,line in enumerate(f.readlines()):
            text= line.split(" ")
            dic_item_template={}
            if( int(text[1])==-1):
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=0
                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.view_index.append(index)
            else:
                dic_item_template["path"]=text[0]
                dic_item_template["flag"]=1
                dic_item_template["left_top"]=(int(float(text[1])),int(float(text[2])) )
                dic_item_template["bottom_right"]=(int(float(text[3])),int(float(text[4])) )
                dic_item_template["eye_l"]=(int(float(text[5])),int(float(text[6])) )
                dic_item_template["eye_r"]=(int(float(text[7])),int(float(text[8])) )
                dic_item_template["nose"]=(int(float(text[9])),int(float(text[10])) )
                dic_item_template["mouth_l"]=(int(float(text[11])),int(float(text[12])) )
                dic_item_template["mouth_r"]=(int(float(text[13])),int(float(text[14])) )
                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.view_index.append(index)
                    
            self.infor_list.append(dic_item_template)
            
        if  self.view_mode==VIEW_MODE_RANDOM:
            self.view_index=random.sample(self.view_index,1000)
      
    def read(self):
        pass
    
    def set_data(self,key,data):
        data=data.split(" ")
        index=self.view_index[key]
        self.infor_list[index]["flag"]=1
        self.infor_list[index]["left_top"]=(int(data[0]),int(data[1]) )
        self.infor_list[index]["bottom_right"]=(int(data[2]),int(data[3]) )
        self.infor_list[index]["eye_l"]=(int(data[4]),int(data[5]) )
        self.infor_list[index]["eye_r"]=(int(data[6]),int(data[7]) )
        self.infor_list[index]["nose"]=(int(data[8]),int(data[9]) )
        self.infor_list[index]["mouth_l"]=(int(data[10]),int(data[11]) )
        self.infor_list[index]["mouth_r"]=(int(data[12]),int(data[13]) )
    
    def get_data(self,key):
        item=self.infor_list[self.view_index[key]]
        output="%d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
        return output
    
    
    def is_setValue(self,key):
        return self.infor_list[self.view_index[key]]["flag"]
    
    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.infor_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
            else:
                output="%s %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n"%( \
                item["path"],item["left_top"][0],item["left_top"][1],item["bottom_right"][0],item["bottom_right"][1], 
                item["eye_l"][0],item["eye_l"][1],item["eye_r"][0],item["eye_r"][1],item["nose"][0],item["nose"][1], 
                item["mouth_l"][0],item["mouth_l"][1],item["mouth_r"][0],item["mouth_r"][1])
            f.write( output )
        f.close() 
    
    def disply(self):
        for item in self.view_index:
            print self.infor_list[item]

        
    def __getitem__(self, key):
        return self.infor_list[self.view_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.view_index)-1 or len( self.view_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.infor_list[self.view_index[self.counter-1]]
    
    def __len__(self):
        return len(self.view_index)

def ViewDict(infor_file,filetype=FILETYPE_Face2Point_and_Landmark,mode=VIEW_MODE_UNLABELED):
    if(filetype==FILETYPE_Face2Point_and_Landmark):
        return Face2Point_and_Landmark(infor_file,mode)

    elif(filetype==FILETYPE_FaceRect_and_Landmark):
        return FaceRect_and_Landmark(infor_file,mode)

    elif(filetype==FILETYPE_FaceBBox_and_Landmark):
        return FaceBBox_and_Landmark(infor_file,mode)

    elif(filetype==FILETYPE_Face2Point):
        return Face2Point(infor_file,mode)

    elif(filetype==FILETYPE_FaceRect):
        return FaceRect(infor_file,mode)

    elif(filetype==FILETYPE_FaceBBox):
        return FaceBBox(infor_file,mode)



if __name__=="__main__":
    test=ViewDict("lfwlabel.txt",0) 
    #print test.get_data(0)
    #test.disply()
    #test.set_data(0, "11 22 11 22 11 22 11 22 11 22 11 22 11 22")
    #test.disply()
    #test.save_file()

