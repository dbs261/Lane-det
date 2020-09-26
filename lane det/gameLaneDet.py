import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
img = cv2.imread(r'E:\idk\road main.jpeg')
r,c,_=img.shape
blank = np.zeros((r,c),dtype=np.uint8)
blanktest = np.zeros((r,c),dtype=np.uint8)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gauss=cv2.GaussianBlur(gray,(5,5),0)
canny = cv2.Canny(gauss,0,255)
pts=np.array([[(0,0),(0,int(r/2.5)),(c,int(r/2.5)),(c,0)]])
canny=cv2.fillPoly(canny,pts,(0,0,0))  
lines = cv2.HoughLinesP(canny,6,np.pi/180,0,minLineLength=57,maxLineGap=4) #,minLineLength=57,maxLineGap=3
line_dict = {}
for idx,line in enumerate(lines):
    for x1,y1,x2,y2 in line:
        slope = (y1-y2)/(x1-x2)
        #c = y1-(slope*x1)
        line_dict[idx]={"cord1":(x1,y1),
                   "cord2":(x2,y2),
                   "slope":slope
                   #,"intercept":c
                   }
        cv2.line(blank,(x1,y1),(x2,y2),255,2)

#print(line_dict)

counter = 0
threshold = 0.8
new_line_dict = {}
for vals in line_dict.items():
    slope = list(list(vals[1].items())[2])[1]
    try:
        for vals2 in new_line_dict.items():
            slopePrevious =list(list(vals2[1].items())[2])[1]
            ratio = slope/slopePrevious
            print(ratio,slopePrevious,slopePrevious)
            if not (0.8<ratio and ratio<1.2) or slope==slopePrevious:
                print(counter)
                new_line_dict[counter]={"cord1":(x1,y1),
                                        "cord2":(x2,y2),
                                        "slope":slope
                                        #,"intercept":c
                                        }
                counter+=1

    except:
        print("Empty dict")

print(line_dict.keys())
print(new_line_dict.keys())
cv2.imshow("line",blank)
cv2.waitKey(0)
#cv2.bilateralFilter()