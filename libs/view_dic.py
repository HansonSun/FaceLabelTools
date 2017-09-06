import os,sys
import random
from collections import OrderedDict

VIEW_MODE_ALL=0
VIEW_MODE_UNLABELED=1
VIEW_MODE_LABELED=2
VIEW_MODE_RANDOM=3

class ViewDict(object):

    def __init__(self,lable_file_path,view_mode=VIEW_MODE_UNLABELED):

        self.all_data_list=[]        #store selsected data
        self.display_data_index=[]  #store selsected index

        self.cur_flag=0
        self.counter=0
        self.view_mode=view_mode

        f=open(lable_file_path,"r")
        
        for index,line in enumerate(f.readlines()):
            line=line[:-1]
            text= line.split(" ")
    
            if( int(float(text[1]) )==-1):
                dict_item_tmp=self.parsr_infor_from_text(text)

                if self.view_mode==VIEW_MODE_ALL or  self.view_mode==VIEW_MODE_UNLABELED:
                    self.display_data_index.append(index)
            else:
                dict_item_tmp=self.parsr_infor_from_text(text)

                if self.view_mode==VIEW_MODE_LABELED or self.view_mode==VIEW_MODE_RANDOM or self.view_mode==VIEW_MODE_ALL:
                    self.display_data_index.append(index)
                    
            self.all_data_list.append(dict_item_tmp)#store all the selected data

        if  self.view_mode==VIEW_MODE_RANDOM:
            self.display_data_index=random.sample(self.display_data_index,1000)
    
    def parsr_infor_from_text(self,text):
        point_cnt=0
        rect_cnt=0
        output_dict=OrderedDict()

        f=open("BBox_5PointsLandmark.txt")
        rules=f.read()
        rules=rules[:-1]
        rule_list=rules.split(",")


        if( int(float(text[1]) )==-1):
            output_dict["path"]=text[0]
            output_dict["flag"]=0

        else:
            output_dict["path"]=text[0]
            output_dict["flag"]=1

            num_index=1
            rule_index=0

            while num_index<len(text):

                if(rule_list[rule_index]=='xy_bbox'):
                    rect_cnt+=1
                    output_dict["rect_%d"%rect_cnt]=((int(float(text[num_index])),int(float(text[num_index+2])) ),(int(float(text[num_index+1])),int(float(text[num_index+3])) ))
                    num_index+=4
                    rule_index+=1
                if(rule_list[rule_index]=='yx_bbox'):
                    rect_cnt+=1
                    output_dict["rect_%d"%rect_cnt]=((int(float(text[num_index+2])),int(float(text[num_index])) ),(int(float(text[num_index+3])),int(float(text[num_index+1])) ))
                    num_index+=4
                    rule_index+=1
                elif( rule_list[rule_index]=='rect'):
                    rect_cnt+=1
                    output_dict["rect_%d",rect_cnt]=((int(float(text[num_index])),int(float(text[num_index+1])) ),\
                    (int(float(text[num_index+3]))+int(float(text[num_index])),int(float(text[num_index+4]))+int(float(text[num_index+1]))  ))
                    num_index+=4
                    rule_index+=1
                elif(rule_list[rule_index]=='point'):
                    point_cnt+=1
                    output_dict["point_%d"%point_cnt]=(int(float(text[num_index])),int(float(text[num_index+1])) )
                    num_index+=2
                    rule_index+=1
                elif(rule_list[rule_index]=='rect2p'):
                    rect_cnt+=1
                    output_dict["rect_%d"%rect_cnt]=((int(float(text[num_index])),int(float(text[num_index+1])) ),(int(float(text[num_index+2])),int(float(text[num_index+3])) ))
                    num_index+=4
                    rule_index+=1

        return output_dict
    

    def read(self):
        pass
    
    def set_data(self,display_index,data):
        data=data.split(" ")
        real_index=self.display_data_index[display_index]
        self.all_data_list[real_index]=self.parsr_infor_from_text(data)


    def is_setValue(self,index):
        return self.all_data_list[self.display_data_index[index]]["flag"]
    


    def save_file(self):
        f=open("resultnew.txt","w")
        for item in self.all_data_list:
            if( item["flag"]==0):
                output="%s %d\n"%(item["path"],-1)
                print output
            else:
                output=""
                for index,key in enumerate(item):
                    if(key!='flag'):
                        if( index!=len(item)-1 ):
                            if( key.find('point')==0 ):
                                output+=str(item[key][0])+" "
                                output+=str(item[key][1])+" "
                            elif(key.find('rect')==0):
                                output+=str(item[key][0][0])+" "
                                output+=str(item[key][0][1])+" "
                                output+=str(item[key][1][0])+" "
                                output+=str(item[key][1][1])+" "
                            elif(key.find('path')==0):
                                output+=str(item[key])+" "
                        else:
                            if( key.find('point')==0 ):
                                output+=str(item[key][0])+" "
                                output+=str(item[key][1])+"\n"
                            elif(key.find('rect')==0):
                                output+=str(item[key][0][0])+" "
                                output+=str(item[key][0][1])+" "
                                output+=str(item[key][1][0])+" "
                                output+=str(item[key][1][1])+"\n"
                            elif(key.find('path')==0):
                                output+=str(item[key])+"\n"

        f.write( output )
        f.close() 


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
    test=ViewDict("testImageList.txt",1) 
    test.set_data(0,"lfw_5590/Abid_Hamid_Mahmud_Al-Tikriti_0001.jpg 78 164 87 173 109.250000 114.250000 144.250000 114.250000 122.250000 136.250000 109.750000 151.750000 138.750000 154.250000")
    test.disply()
    #test.save_file()
    #print test.is_setValue(1)
    #test.disply()
    #test.set_data(0, "11 22 11 22 11 22 11 22 11 22 11 22 11 22")
    #test.disply()
    #test.save_file()

