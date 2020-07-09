#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import sys
#reload(sys)
#sys.setdefaultencoding('UTF8')

import numpy as np
import cv2
import time
import os
from urllib.request import urlopen
from imutils.video import FileVideoStream
from resize1 import resize

number_of_windows = 4
in_dir = '/home/alexander/Документы/camera/raw/1752/'
files = os.listdir(in_dir)

H = 1080
W = 1920
h0 = 0
w0 = 80
y_correction = 55
if number_of_windows <= 4:
    pos = [[w0, h0+y_correction], [w0+int((W-w0)/2), h0+y_correction], [w0, h0+int((H-h0)/2)+y_correction], [w0+int((W-w0)/2), h0+int((H-h0)/2)+y_correction]]
elif number_of_windows > 4:
    pos = [[w0, h0+y_correction], [w0+int((W-w0)/3), h0+y_correction], [w0+int(2*(W-w0)/3), h0+y_correction], [w0, h0+int((H-h0)/2)+y_correction], [w0+int((W-w0)/3), h0+int((H-h0)/2)+y_correction], [w0+int(2*W/3), h0+int((H-h0)/2)+y_correction]]
file_no = -1
in_use = []
cap = []
win_name = []
for i in range(number_of_windows):
    in_use.append(False)
    cap.append(None)
    win_name.append(None)

while True:
    for window_no in range(number_of_windows):
        if in_use[window_no] == False:
            file_no += 1
            print("opening " + str(files[file_no]))
            cap[window_no] = cv2.VideoCapture(in_dir + str(files[file_no]))
            #file_name.append((str(file)).split('.')[0])
            if not cap[window_no].isOpened():
                print("no video" + str(files[file_no]))
                #in_use[window_no] = False
                continue
            print("started: " + str(files[file_no]))
            cv2.namedWindow(str(files[file_no]), cv2.WINDOW_NORMAL)
            if number_of_windows <= 4:
                cv2.resizeWindow(str(files[file_no]), int((W-w0)/2), int((H-h0)/2)-y_correction)
            if number_of_windows > 4:
                cv2.resizeWindow(str(files[file_no]), int((W-w0)/3), int((H-h0)/2)-y_correction)
            cv2.moveWindow(str(files[file_no]), pos[window_no][0], pos[window_no][1])
            in_use[window_no] = True
            win_name[window_no] = str(files[file_no])
        else:
            ret, frame = cap[window_no].read()
            if frame is None:
                for i in range(4):
                    cap[window_no].release()
                cv2.destroyWindow(win_name[window_no])
                in_use[window_no] = False
                continue
            frame = cv2.resize(frame, (640, 480))
            cv2.imshow(win_name[window_no], frame)

    key = cv2.waitKey(1)
    if (key == ord("q")) or (key == 27):
        break
    if (key == ord("m")):
        #time.sleep(1)
        while True:
            key = cv2.waitKey(1)
            if (key == ord("m")):
                break
            #time.sleep(1)
cv2.destroyAllWindows()
