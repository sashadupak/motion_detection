#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import sys
#reload(sys)
#sys.setdefaultencoding('UTF8')

import numpy as np
import cv2
import time
import os
import json

number_of_windows = 12
in_dir = '/home/alexander/Документы/camera/raw/1752/'
log_file_name = 'used_video_files.json'
H = 1080
W = 1920

if number_of_windows == 1:
    n, m = 1, 1
elif number_of_windows <= 4:
    n, m = 2, 2
elif number_of_windows <= 6:
    n, m = 2, 3
elif number_of_windows <= 8:
    n, m = 2, 4
elif number_of_windows == 9:
    n, m = 3, 3
elif number_of_windows <= 12:
    n, m = 3, 4
else:
    print("incorrect number of windows")
    exit(0)

default_img = np.zeros((480, 640, 3), np.uint8)
files = os.listdir(in_dir)
file_no = -1
in_use = []
cap = []
win_name = []
for i in range(number_of_windows):
    in_use.append(False)
    cap.append(None)
    win_name.append(None)
used_video_files = {}
quit = False

cv2.namedWindow("frames", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frames", W, H)
cv2.moveWindow("frames", 0, 0)

finish = 0
while True:
    frames = []
    for window_no in range(number_of_windows):
        if in_use[window_no] == False:
            file_no += 1
            if file_no < len(files):
                win_name[window_no] = str(files[file_no])
                if win_name[window_no] not in used_video_files.keys():
                    cap[window_no] = cv2.VideoCapture(in_dir + str(files[file_no]))
                    if not cap[window_no].isOpened():
                        print("no video" + str(files[file_no]))
                        frames.append(default_img)
                        continue
                    print("opened: " + str(files[file_no]))
                    used_video_files.update({win_name[window_no]: "opened"})
                    in_use[window_no] = True
            frames.append(default_img)
        else:
            ret, frame = cap[window_no].read()
            if frame is None:
                cap[window_no].release()
                print("closed " + win_name[window_no])
                used_video_files.update({win_name[window_no]: "closed"})
                in_use[window_no] = False
                frames.append(default_img)
                continue
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.putText(frame, win_name[window_no], (50,50), cv2.FONT_HERSHEY_SIMPLEX ,  
                   1, (255, 255, 255), 2, cv2.LINE_AA) 
            frames.append(frame)
        if in_use[window_no] == False:
            finish += 1
        else:
            finish = 0
    if finish >= number_of_windows:
        break
    if len(frames) > 0:
        col = []
        for i in range(n):
            row = []
            for j in range(m):
                row.append(frames[i*m+j])
            col.append(cv2.hconcat(row))
        image = cv2.vconcat(col)
        cv2.imshow("frames", image)
    
    key = cv2.waitKey(1)
    if (key == ord("q")) or (key == 27):
        break
    if (key == 0x20):
        while True:
            key = cv2.waitKey(1)
            if (key == 0x20):
                break
            if (key == ord("q")) or (key == 27):
                quit = True
                break
        if quit == True:
            break

with open(log_file_name, 'w') as fp:
    json.dump(used_video_files, fp)
cv2.destroyAllWindows()
