import cv2
import numpy as np
import math
import os

#rotate the point according to the center
def rotate_points(points, center, angle,scale=1):
    angle=angle * math.pi / 180
    dst=[]
    for point in points:
        tmp_point=[0,0]
        x = point[0] - center[0]
        y = point[1] - center[1]
        tmp_point[0] = int(x * math.cos(angle)*scale + y * math.sin(angle)*scale + center[0])
        tmp_point[1] = int(-x * math.sin(angle)*scale+ y * math.cos(angle)*scale + center[1])
        dst.append( tuple(tmp_point) )
    return dst

def rotate_img_and_points(src,points,scale=1):
    angle= math.atan( ( (points[1][1]-points[0][1])*1.0/(points[1][0]-points[0][0]) ) )* 180 /math.pi
    center=(float(points[2][0]),float(points[2][1]))
    M=cv2.getRotationMatrix2D( center,angle,scale)
    dst=cv2.warpAffine(src,M,(src.shape[1],src.shape[0]))
    points=rotate_points(points, center, angle,scale)
    return dst,points

def face_align(face,points):
    r=abs(int( (points[0][1]-points[3][1])*0.6) ) 
    #r=20
    h1=int(points[0][1]-r) if int(points[0][1]-r)>0 else 0
    h2=int(points[3][1]+r) if int(points[3][1]+r)<face.shape[0] else face.shape[0]
    w1=int(points[0][0]-r) if int(points[0][0]-r)>0  else 0
    w2=int(points[1][0]+r) if int(points[1][0]+r)<face.shape[1] else face.shape[1]
    roi_img=face[h1:h2,w1:w2]
    return roi_img


if __name__ =="__main__":

    newroot_dir="lfw-ALIGN-GRAY-128x128"


    if not os.path.exists(newroot_dir):
        os.mkdir(newroot_dir)

    f=open("resultnew.txt","r")
    for index,line  in enumerate (f.readlines( )):
        line = line[:-1]
        all_infor=line.split(' ')
        if len(all_infor)==15:
            img_path=all_infor[0]
            l_eye=(int(all_infor[5]),int(all_infor[6]) )
            r_eye=(int(all_infor[7]),int(all_infor[8]) )
            nose=(int(all_infor[9]),int(all_infor[10]) )
            l_mouth=(int(all_infor[11]),int(all_infor[12]) )
            r_mouth=(int(all_infor[13]) ,int(all_infor[14]) )
        
            p=(l_eye,r_eye,nose,l_mouth,r_mouth)

        img=cv2.imread(img_path,0)
        img,p=rotate_img_and_points(img,p,1)
        img=face_align(img,p)
        img=cv2.resize(img,(128,128))


        person_name=img_path.split("/")[1]
        print person_name
        new_img_dir=os.path.join(newroot_dir,person_name)

        if(not os.path.exists(new_img_dir)):
            os.mkdir(new_img_dir)
        file_name=img_path.split("/")[-1]
        new_img_path=os.path.join(new_img_dir,file_name) 
        print new_img_path

        cv2.imwrite(new_img_path,img)

