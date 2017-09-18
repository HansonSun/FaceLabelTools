import os,sys
import random
from collections import OrderedDict
import time
import init

VIEW_MODE_ALL=0
VIEW_MODE_UNLABELED=1
VIEW_MODE_LABELED=2
VIEW_MODE_RANDOM=3


class ViewDict(object):

    def __init__(self,view_mode=VIEW_MODE_UNLABELED):
        
        self.all_data_list=[]        #store selsected data
        self.display_data_index=[]   #store selsected index
        self.cur_flag=0
        self.counter=0
        self.view_mode=view_mode

        #get label file's dir and basename
        self.label_file_dir,self.label_file_name=os.path.split( init.glb_label_file )

        with open(init.glb_label_file ,"r") as f:
        
            for index,line in enumerate(f.readlines()):

                line=line.strip()
                one_label=line.split(" ")
        
                if( int(float(one_label[1]) )==-1):
                    dict_item_tmp=self.parsr_infor_from_text(one_label)

                    if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                        self.display_data_index.append(index)

                else:
                    dict_item_tmp=self.parsr_infor_from_text(one_label)

                    if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                        self.display_data_index.append(index)
                        
                self.all_data_list.append(dict_item_tmp)#store all the selected data

            if  self.view_mode==VIEW_MODE_RANDOM:
                self.display_data_index=random.sample(self.display_data_index,1000)


    def parsr_infor_from_text(self,text):
        point_cnt=0
        rect_cnt=0
        output_dict=OrderedDict()


        if( int(float(text[1]) )==-1):
            output_dict["path"]=os.path.join(self.label_file_dir,text[0])
            output_dict["flag"]=0

        else:
            output_dict["path"]=os.path.join(self.label_file_dir,text[0])
            output_dict["flag"]=1

            num_index=1
            rule_index=0

            while num_index<len(text):

                if(init.glb_input_rule_list[rule_index]=='xy_bbox'):
                    rect_cnt+=1
                    output_dict["rect2p_%d"%rect_cnt]=((int(float(text[num_index])),int(float(text[num_index+2])) ),(int(float(text[num_index+1])),int(float(text[num_index+3])) ))
                    num_index+=4
                    rule_index+=1
                if(init.glb_input_rule_list[rule_index]=='yx_bbox'):
                    rect_cnt+=1
                    output_dict["rect2p_%d"%rect_cnt]=((int(float(text[num_index+2])),int(float(text[num_index])) ),(int(float(text[num_index+3])),int(float(text[num_index+1])) ))
                    num_index+=4
                    rule_index+=1
                elif(init.glb_input_rule_list[rule_index]=='rect'):
                    rect_cnt+=1
                    output_dict["rect2p_%d"%rect_cnt]=((int(float(text[num_index])),int(float(text[num_index+1])) ),\
                    (int(float(text[num_index+2]))+int(float(text[num_index])),int(float(text[num_index+3]))+int(float(text[num_index+1]))  ))
                    num_index+=4
                    rule_index+=1
                elif(init.glb_input_rule_list[rule_index]=='point'):
                    point_cnt+=1
                    output_dict["point_%d"%point_cnt]=(int(float(text[num_index])),int(float(text[num_index+1])) )
                    num_index+=2
                    rule_index+=1
                elif(init.glb_input_rule_list[rule_index]=='rect2p'):
                    rect_cnt+=1
                    output_dict["rect2p_%d"%rect_cnt]=((int(float(text[num_index])),int(float(text[num_index+1])) ),(int(float(text[num_index+2])),int(float(text[num_index+3])) ))
                    num_index+=4
                    rule_index+=1

        return output_dict
    

    def read(self):
        pass
    
    def set_data(self,display_index,data):
        real_index=self.display_data_index[display_index]
        self.all_data_list[real_index].update(data)


    def is_setValue(self,index):
        return self.all_data_list[self.display_data_index[index]]["flag"]
    


    def save_file(self):
        file_only_name=self.label_file_name.split('.')[0]
        cur_time=time.strftime("%m_%d_%H_%M", time.localtime()) 

        with open("result/label_file_output/%s_%s.txt"%(file_only_name,cur_time),"w") as f:
            output=""
            for item in self.all_data_list:
                rule_index=0
                if( item["flag"]==0):
                    output+="%s %d\n"%(item["path"],-1)

                else:
                    for index,key in enumerate(item):
                        
                        if(key=="path"):
                            output+=str(item[key])+" "
                            continue
                        else:
                            if(key!='flag'):
                                if( key.find('point')==0 ):
                                    output+=str(item[key][0])+" "
                                    output+=str(item[key][1])+" "
                                elif(key.find('rect')==0):
                                    if(   init.glb_output_rule_list[rule_index]=='rect' ):
                                        output+=self.convert_rect2p_to_rect(item[key])
                                    elif( init.glb_output_rule_list[rule_index]=='xy_bbox'):
                                        output+=self.convert_rect2p_to_xy_bbox(item[key])
                                rule_index+=1
                                if(rule_index==len(init.glb_output_rule_list) ):
                                    output+="\n"

                                

            f.write( output )

        
    def convert_rect2p_to_rect(self,points):
        return "%d %d %d %d "%(points[0][0],points[0][1],points[1][0]-points[0][0],points[1][1]-points[0][1])

    def convert_rect2p_to_xy_bbox(self,points):
        return "%d %d %d %d "%(points[0][0],points[1][0],points[0][1],points[1][1])

    def get_data(self,key):
        item=self.all_data_list[self.display_data_index[key]]
        return item

    def disply(self):
        for item in self.display_data_index:
            print self.all_data_list[item]

        
    def __getitem__(self, key):
        return self.all_data_list[self.display_data_index[key]]
    
    def __iter__(self):
        return self

    def next(self): 
        if self.counter > len( self.display_data_index)-1 or len( self.display_data_index)==0:
            self.counter=0 
            raise StopIteration();
        self.counter+=1
        return self.all_data_list[self.display_data_index[self.counter-1]]
    
    def __len__(self):
        return len(self.display_data_index)
   



if __name__=="__main__":
    test=ViewDict("testImageList.txt","BBox_5PointsLandmark.txt",0)

    test.disply()
   
    test.save_file("BBox_5PointsLandmark.txt")
