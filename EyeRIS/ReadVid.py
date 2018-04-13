# Import external libraries (must be installed)
import numpy as np
import cv2
#import os
import Tkinter
import tkFileDialog as fd

# pick using GUI
Tkinter.Tk().withdraw() # Close the root window
InputStream = fd.askopenfilename()
cap = cv2.VideoCapture(InputStream)
# main loop for frame-by-frame analysis
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    (thresh, im_bw) = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY)

    # Display the resulting frame
    cv2.imshow('binary', im_bw)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()