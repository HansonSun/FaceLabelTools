from ctypes import *
import numpy as np
import cv2
import time
import os
import sys
import shutil

class facetool (object):
	def __init__(self):
		#file_path= os.path.split(os.path.realpath(__file__))[0]
		self.facelib = cdll.LoadLibrary("./lib/facedetect.so" ) 
		#self.facelib = np.ctypeslib.load_library("facedetectTool", ".")
		self.facelib.greet()
		self.facetool=self.facelib.creat_facetool()
		
	def findFaces(self,img_path,is_show):
		FaceDataType =c_int*80
		face_data=FaceDataType()
		face_cnt=c_int()
		p_face_cnt=pointer(face_cnt)
		self.facelib.findFaces(self.facetool,img_path,p_face_cnt,face_data,is_show)
		
		face_list=[]
		
		for i in range(face_cnt.value):
			face_dict={}
			face_dict['x']=face_data[4*i+0]
			face_dict['y']=face_data[4*i+1]
			face_dict['w']=face_data[4*i+2]
			face_dict['h']=face_data[4*i+3]
			face_list.append(face_dict)
		return face_list
	
	def showImg(self,img_path):
		return self.facelib.showImg(self.facetool,img_path)

		
	def Alignface_with5p(self,img_path,is_show=0,new_path=''):
		face_cnt=self.facelib.Alignface_with5p(self.facetool,img_path )
		if face_cnt <0:

			return -1
		else :
			tmp_img=cv2.imread("~tmp~.jpg",0)
			tmp_img=cv2.resize(tmp_img, (128,128) )
			if is_show==1:
				cv2.imshow("ww",tmp_img)
				cv2.waitKey(0)
			
			if new_path!='':
				cv2.imwrite(new_path,tmp_img)
				#shutil.move("~tmp~.jpg",new_path)
			else :
				os.remove("~tmp~.jpg")
			
			return 1
		
	
	def getAbs5pFromImg(self,img_path,is_show=0):
		LandmarkDataType =c_int*200
		lanmark_data=LandmarkDataType()
		face_cnt=c_int()
		p_face_cnt=pointer(face_cnt)
		self.facelib.getAbs5pFromImg(self.facetool,img_path,p_face_cnt,lanmark_data,is_show)
		
		face_list=[]
		for i in range(face_cnt.value):
			face_dict={}
			face_dict['l_eye']=(lanmark_data[10*i+0],lanmark_data[10*i+1])
			face_dict['r_eye']=(lanmark_data[10*i+2],lanmark_data[10*i+3])
			face_dict['nose']=(lanmark_data[10*i+4],lanmark_data[10*i+5])
			face_dict['l_mouth']=(lanmark_data[10*i+6],lanmark_data[10*i+7])
			face_dict['r_mouth']=(lanmark_data[10*i+8],lanmark_data[10*i+9])
			face_list.append(face_dict)
		return face_list
		
	def getRel5pFromImg(self,img_path,is_show):
		self.facelib.getRel5pFromImg(self.facetool,img_path,is_show)
		
	def getRel5pFromFace(self,img_path,is_show):
		self.facelib.getRel5pFromFace(self.facetool,img_path,is_show)
		
	def getAbs68pFromImg(self,img_path,is_show):
		self.facelib.getAbs68pFromImg(self.facetool,img_path,is_show)
		
	def getRel68pFromImg(self,img_path,is_show):
		self.facelib.getRel68pFromImg(self.facetool,img_path,is_show)
		
	def getRel68pFromFace(self,img_path,is_show):
		self.facelib.getRel68pFromFace(self.facetool,img_path,is_show)

		
if __name__=="__main__":
	detector=facetool()
	print detector.findFaces("Aaron_Eckhart_0001.jpg",1)
	print detector.getAbs5pFromImg("Aaron_Eckhart_0001.jpg")

