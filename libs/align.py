from ctypes import *
import numpy as np
import cv2
import time
import os
import sys
import math
from facedetect_lib import facetool

detector=facetool()
root_dir="lfw-deepfunneled"
newroot_dir="lfw-ALIGN-GRAY-128x128"


if not os.path.exists(newroot_dir):
	os.mkdir(newroot_dir)
	
for root,dir,files in os.walk(root_dir):
	for file in files:
		imgpath=os.path.join(root,file)

		face_infor=detector.findFaces(imgpath,0)
		if len(face_infor)>1:
			img=cv2.imread(imgpath,0)
			mid_point=(img.shape[0]/2,img.shape[1]/2)
			distance_list=[]
		
			for infor in face_infor:
				infor_mid_P=(infor['x']+infor['w']/2,infor['y']+infor['h']/2)
				distance_list.append(pow(infor_mid_P[0]-mid_point[0],2) + pow(infor_mid_P [1] -mid_point[1],2))

			roi_index=distance_list.index(min(distance_list))
			roi_face=img[ face_infor[roi_index]['y']:face_infor[roi_index]['y']+face_infor[roi_index]['h'],face_infor[roi_index]['x']:face_infor[roi_index]['x']+face_infor[roi_index]['w'] ]
						

		elif len(face_infor)==1:
			img=cv2.imread(imgpath,0)
			roi_face=img[ face_infor[0]['y']:face_infor[0]['y']+face_infor[0]['h'],face_infor[0]['x']:face_infor[0]['x']+face_infor[0]['w'] ]

		elif len(face_infor)==0:
			img=cv2.imread(imgpath,0)
			roi_face=img[ 61:189,61:189 ]
			


		person_name=root.split("/")[1]
		new_img_dir=os.path.join(newroot_dir,person_name)
		
		if(not os.path.exists(new_img_dir)):
			os.mkdir(new_img_dir)
		new_img_path=os.path.join(new_img_dir,file) 
		print new_img_path

		roi_face=cv2.resize(roi_face,(128,128))
		cv2.imwrite(new_img_path,roi_face)
