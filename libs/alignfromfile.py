import sys 
import os
import shutil
import cv2
import numpy as np
import math
import commands
import faceAugment
from conda.config import root_dir


def distance( (x1,y1),(x2,y2) ):
	return math.sqrt( (y2-y1)*(y2-y1)+(x2-x1)*(x2-x1) )


def face_align(face,points):
	r=abs(int( (points[0][1]-points[3][1])*0.6) ) 
	#r=20
	h1=int(points[0][1]-r) if int(points[0][1]-r)>0 else 0
	h2=int(points[3][1]+r) if int(points[3][1]+r)<face.shape[0] else face.shape[0]
	w1=int(points[0][0]-r) if int(points[0][0]-r)>0  else 0
	w2=int(points[1][0]+r) if int(points[1][0]+r)<face.shape[1] else face.shape[1]
	roi_img=face[h1:h2,w1:w2]
	return roi_img


def align_and_save(new_dir):

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
		l_eye=(int(infor[5]),int(infor[6]))
		r_eye=(int(infor[7]),int(infor[8]) )
		nose=(int(infor[9]),int(infor[10]) )
		l_mouth=(int(infor[11]),int(infor[12]))
		r_mouth=(int(infor[13]),int(infor[14]) )
		get_landmarks(path_name,new_file_name,(l_eye,r_eye,nose,l_mouth,r_mouth) )
		
		#break


align_and_save("CASIA-WebFace-RN-Align")

