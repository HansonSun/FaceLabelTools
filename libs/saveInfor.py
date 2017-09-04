import sys
import os

def read_file(file_path):
    with open(file_path) as f:
        infor=f.read()
        
def write_file(img_name,points):
    with open("result/%s.txt"%img_name) as f:
        output="img_name"
        f.write(output)
        
if __name__=="__main__":
    #read_file("www.txt")
    a=[1,2,3]
    b='.'.join(a)
    print b
     