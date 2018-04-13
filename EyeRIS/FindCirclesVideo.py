# Import external libraries (must be installed)
import numpy as np
import cv2
import argparse
#import os
import Tkinter
import tkFileDialog as fd
## pick file
# pick using GUI
Tkinter.Tk().withdraw() # Close the root window
InputStream = fd.askopenfilename()
# or pick from defined path
# BaseDir = "E:/Documents/MATLAB/Data/hPDR_data/Baby_hPDR/2016/"
# SubjDir = "171109_B030/"
# CamDir = "171109_B030_01_MC2/"
# VidFile = "171109_B030_01_001_S1.avi"
#InputStream = (BaseDir+SubjDir+CamDir+VidFile)
# grab video from file or camera
cap = cv2.VideoCapture(InputStream)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #copy frame, convert to grayscale
    output = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #find circles
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 200,param1=20,param2=20,minRadius=10,maxRadius=16)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 1)
            cv2.rectangle(output, (x - 2, y - 2), (x + 2, y + 2), (0, 128, 255), -1)

    # show the output image
    cv2.imshow("output", np.hstack([frame, output]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#
#     # Our operations on the frame come here
#     # threshold 'frame' to grayscale using second ind
#     (thresh, im_bw) = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY)
#
#     #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # Display the resulting frame
#     cv2.imshow('binary', im_bw)
#     #cv2.imshow('frame',)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()
# unused code
# ret, frame = video_capture.read()
# #cv2.imshow('frame',frame)
# #cv2.waitKey(0)
# (thresh, im_bw) = cv2.threshold(frame, 192, 255, cv2.THRESH_BINARY)
# cv2.imshow('binary',im_bw)
# cv2.waitKey(0)
## some copied code for vid processing
##import cv2
##import numpy as np
##from matplotlib import pyplot as plt
##
##im=cv2.imread('1.jpg')
###mask=np.zeros(img.shape[:2],np.uint8)
##imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##ret,thresh=cv2.threshold(imgray,200,200,200)
##countours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
##
##cv2.drawContours(im,countours,-1,(0,255,0),3)
##cv2.imshow("begueradj",im)
##cv2.waitKey(0)
##cv2.destroyAllWindows()
