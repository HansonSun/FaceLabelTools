from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
from facedetect_lib import  facetool
import cv2
import os

class GenerateLabelFile(QThread):
	def __init__(self,detector,absdirname,parent=None):
		super(GenerateLabelFile,self).__init__(parent)
		self.detector=detector
		self.absdirname=absdirname

	def run(self):
		dirname=self.absdirname.split("/")[-1]

		with open("result/labeled_label_file/labeled_%s.txt"%dirname,"a") as f:	
			for root,subdir,files in os.walk(self.absdirname):
				for img_file in files:
					tmp_dir=root[root.find(dirname):]
					img_path=os.path.join(root,img_file)

					facerect_list= self.detector.findFaces(img_path,0)
					facelandmark_list= self.detector.getAbs5pFromImg(img_path)
					
					wrstr=""

					if len(facerect_list)>1:

						img=cv2.imread(img_path,0)
						mid_point=(img.shape[0]/2,img.shape[1]/2)
						distance_list=[]

						for facerect in facerect_list:
							infor_mid_P=(facerect['x']+facerect['w']/2,facerect['y']+facerect['h']/2)
							distance_list.append(pow(infor_mid_P[0]-mid_point[0],2) + pow(infor_mid_P [1] -mid_point[1],2))

						faceindex=distance_list.index(min(distance_list))

						wrstr="%s %s %s %s %s %d %d %d %d %d %d %d %d %d %d\n"%(os.path.join(tmp_dir,img_file),\
							facerect_list[faceindex]['x'],facerect_list[faceindex]['y'],facerect_list[faceindex]['w'],facerect_list[faceindex]['h'],\
							facelandmark_list[faceindex]['l_eye'][0],facelandmark_list[faceindex]['l_eye'][1],facelandmark_list[faceindex]['r_eye'][0],facelandmark_list[faceindex]['r_eye'][1],\
							facelandmark_list[faceindex]['nose'][0],facelandmark_list[faceindex]['nose'][1],facelandmark_list[faceindex]['l_mouth'][0],facelandmark_list[faceindex]['r_mouth'][1],\
							facelandmark_list[faceindex]['r_mouth'][0],facelandmark_list[faceindex]['r_mouth'][1] )
						print wrstr		

					elif len(facerect_list)==1:

						wrstr="%s %s %s %s %s %d %d %d %d %d %d %d %d %d %d\n"%(os.path.join(tmp_dir,img_file),\
							facerect_list[0]['x'],facerect_list[0]['y'],facerect_list[0]['w'],facerect_list[0]['h'],\
							facelandmark_list[0]['l_eye'][0],facelandmark_list[0]['l_eye'][1],facelandmark_list[0]['r_eye'][0],facelandmark_list[0]['r_eye'][1],\
							facelandmark_list[0]['nose'][0],facelandmark_list[0]['nose'][1],facelandmark_list[0]['l_mouth'][0],facelandmark_list[0]['r_mouth'][1],\
							facelandmark_list[0]['r_mouth'][0],facelandmark_list[0]['r_mouth'][1] )
						print wrstr	

					elif len(facerect_list)==0:
						wrstr="%s -1\n"%(os.path.join(tmp_dir,img_file) )
					
					f.write(wrstr)

		print "label finish"