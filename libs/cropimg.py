import sys 
import os
import shutil
import cv2
import numpy as np
import math
import commands
import faceAugment



def crop_and_save(new_dir):

	f=open("saved_result/result.txt","r")
	if not os.path.exists(new_dir):
			os.mkdir(new_dir)
	for text in f.readlines():
		#print text
		infor=text.split(" ")
		path_name=infor[0]
		root_dir,subdir,filename=path_name.split("/")
		
		if not os.path.exists(os.path.join(new_dir,subdir) ):
			os.mkdir(os.path.join(new_dir,subdir))
		print os.path.join(new_dir,subdir)
		
		new_file_name=os.path.join(new_dir,subdir,filename)
		
		#print new_file_name
		lt_x=(int(infor[5]),int(infor[6]))
		lt_y=(int(infor[5]),int(infor[6]))
		rb_x=(int(infor[5]),int(infor[6]))
		rb_y=(int(infor[5]),int(infor[6]))

		face_roi=img[lt_y:rb_y,lt_x:rb_x]
		
		cv2.imshow("test",face_roi)
		cv2.waitKey(0)


align_and_save("lfw-Align")

