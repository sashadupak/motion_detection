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

def run(in_file, out_dir, visible=False):
    original = in_file #'/home/alexander/Документы/camera/raw/0904/00010000906000200.mp4'
    #resized = '/home/alexander/Документы/camera/raw/1004/s4.mp4'
    outpath = out_dir #/home/alexander/Документы/camera/raw/1752/'

    in_file_name = (original.split('/')[-1]).split('.')[0]
    sh = open(out_dir + in_file_name + '.txt', 'w')

    #resize(original, resized, 640, 480, 5.0)

    """
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 960,720)
    cv2.moveWindow('frame', 0,0)
    cv2.namedWindow('processing', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('processing', 960,720)
    cv2.moveWindow('processing', 1000,0)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('4', cv2.WINDOW_NORMAL)
    """
    backSub = cv2.createBackgroundSubtractorKNN()
    filename = 0
    begin = None
    end = None
    frame = None
    count = 0
    x_old = None
    y_old = None
    avg = None
    motion = False
    print("opening video stream...")
    cap = cv2.VideoCapture(original)
    #vs = FileVideoStream(inpath).start()
    fps = cap.get(cv2.CAP_PROP_FPS)
    #print(fps)
    H = 480#int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    W = 640#int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    if not cap.isOpened():
        print("no video")
        exit()
    cur_frame = 0
    print("started: " + str(in_file_name))

    while True:
        cur_frame += 1
        ret, frame = cap.read()
        #frame = vs.read()
        if frame is None:
            break
        frame = cv2.resize(frame, (640, 480))
        if motion == True:
            out.write(frame)
        if True:
            #image = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fgMask = backSub.apply(frame)
            if avg is None:
                avg = frame.copy().astype(float)
            cv2.accumulateWeighted(frame, avg, 0.5)
            delta_frame = cv2.absdiff(cv2.convertScaleAbs(avg), frame)
            #"""
            contours = np.array([(520,480), (0,90), (0, 480), (520, 480)])
            cv2.fillPoly(delta_frame, pts =[contours], color=(0))
            cv2.fillPoly(fgMask, pts =[contours], color=(0))
            contours = np.array([(640,200),(200,0), (640, 0), (640, 200)])
            cv2.fillPoly(delta_frame, pts =[contours], color=(0))
            cv2.fillPoly(fgMask, pts =[contours], color=(0))
            cv2.circle(delta_frame, (0,0), 200, (0), -1) 
            cv2.circle(fgMask, (0,0), 200, (0), -1) 
            #"""
            thresh = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            #kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            opening = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
            combo = closing | opening
            contours, h = cv2.findContours(combo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(image, contours, -1, (255, 0, 0), 3, cv2.LINE_AA, h, 1)
            contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
            if len(contour_sizes) > 0:#for cnt in contours:
                #if cv2.contourArea(cnt) < 100:
                #    continue
                cnt = max(contour_sizes, key=lambda x: x[0])[1]  # the biggest contour
                cnt = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                cnt = cv2.convexHull(cnt)
                if cv2.contourArea(cnt) > 900:
                    #cv2.drawContours(image, [cnt], -1, (0, 255, 0), 3)
                    x,y,w,h = cv2.boundingRect(cnt)
                    if (w*h) > 900 and (w*h) < 90000:
                        if x_old == None:
                            x_old = x
                            y_old = y
                        if (x_old-20) < x < (x_old+20):
                            if (y_old-20) < y < (y_old+20):
                                count += 1
                                if count > 5:
                                    #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
                                    if begin is None:
                                        begin = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
                                        filename += 1
                                        out = cv2.VideoWriter(outpath + str(in_file_name) + '_segment' + str(filename) + '.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (W, H))
                                        #print("begin: " + str(begin))
                                        motion = True
                                        end = None
                    x_old = x
                    y_old = y
                else:
                    count = 0
                    x_old = None
                    y_old = None
                    if begin is not None:
                        duration = cap.get(cv2.CAP_PROP_POS_MSEC)/1000 - begin
                        #print("duration: " + str(duration))
                        out.release()
                        motion = False
                        if duration < 2:
                            os.remove(outpath + str(in_file_name) + '_segment' + str(filename) + '.avi') 
                            filename -= 1
                            #if begin >= 5:
                            #    begin -= 5
                            #    end += 10
                            #crop(str(begin), str(end), url, u'/home/alexander/Документы/camera/raw/1004/' + str(filename) + '.mp4')
                            #print('Croped ' + str(url) + '. Begin: ' + str(begin) + ', end: ' + str(end))
                        else:
                            print("saved: " + str(filename))
                            sh.write(str(begin) + ' ' + str(begin+duration) + '\n')
                        begin = None

            #cv2.line(image,(520,480),(0,90),(0),2)
            #cv2.line(image,(640,200),(200,0),(0),2)
            #cv2.circle(image, (0,0), 200, (0), 2) 

            if visible:
                cv2.imshow('frame',frame)
                cv2.imshow('processing',combo)
            
            #if cv2.waitKey(1) == 27:
            #    exit(0)
            #time.sleep(0.1)

            key = cv2.waitKey(1)
            if (key == ord("q")) or (key == 27):
                break

    sh.close()
    if filename == 0:
        os.remove(out_dir + in_file_name + '.txt')
    cap.release()
    #vs.stop()
    cv2.destroyAllWindows()
    print("end: " + str(in_file_name))
