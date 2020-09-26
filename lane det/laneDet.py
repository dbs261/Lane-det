import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
#from serialComm import dataTrans as dt
img = cv2.imread(r'road_main.jpeg')
r,c,_=img.shape
blank = np.zeros((r,c),dtype=np.uint8)
blanktest = np.zeros((r,c),dtype=np.uint8)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gauss=cv2.GaussianBlur(gray,(5,5),0)
canny = cv2.Canny(gauss,0,255)
#cv2.imshow("canny",canny)
#pts = np.array([[(0,r),(0,0),(c,0),(c,r),(int(1.5*c/2),int(1.2*r/3)),(int(0.5*c/2),int(1.2*r/3))]], dtype=np.int32)
pts=np.array([[(0,0),(0,int(r/2.5)),(c,int(r/2.5)),(c,0)]])
#imgMas=cv2.fillPoly(img,pts,(0,0,0))
canny=cv2.fillPoly(canny,pts,(0,0,0))  #gray to canny
#cv2.imshow("imgMas",imgMas)
#plt.imshow(canny)
#plt.show()
lines = cv2.HoughLinesP(canny,6,np.pi/180,0)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(blank,(x1,y1),(x2,y2),255,2)
contours,_ = cv2.findContours(blank,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    cv2.drawContours(blanktest,cnt,-1,255)
    cv2.imshow("cnt",blanktest)
    cv2.waitKey(50)
for contour in contours:
    if cv2.contourArea(contour)>cv2.arcLength(contour,True):
        M = cv2.moments(contour)
        cx = int(M["m10"]/M['m00'])
        cy = int(M["m01"]/M['m00'])
        cv2.circle(blank,(cx,cy),2,127,-1)
        print(cx,cy)
        """ if cx in range (int(c/2-15),int(c/2+15)):
            dt(2)
        elif cx>int(c/2):
            dt(3)
        elif cx<int(c/2):
            dt(1) """
        
cv2.imshow("line",blank)
cv2.waitKey(0)
cv2.bilateralFilter()