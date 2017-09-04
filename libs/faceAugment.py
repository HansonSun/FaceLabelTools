import cv2
import numpy as np
import math



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
