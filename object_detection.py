from imutils.video import VideoStream
import numpy as np
import sys
import argparse
import imutils
import time
import cv2
import os
import dlib
from imutils.video import FPS

input_dir = '/home/alexander/Документы/camera/raw/1752/'
video_files = os.listdir(input_dir)

prototxt = 'MobileNetSSD_deploy.prototxt.txt'
model = 'MobileNetSSD_deploy.caffemodel'
min_confidence = 0.5

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt, model)

quit = False
startX = None
fps = FPS().start()

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 640, 480)
cv2.moveWindow("frame", 0, 0)

for video_file in video_files:
    print("[INFO] starting video stream...")
    vs = cv2.VideoCapture(input_dir + str(video_file))

    while True:
        detected_objects = []
        ret, frame = vs.read() 
        if frame is None:
            break
        frame = cv2.resize(frame, (300, 225))
            
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0/127.5, size=(300, 225), mean=[127.5,127.5, 127.5])

        net.setInput(blob)
        #net.setInput(blob, scalefactor=1.0/127.5, mean=[127.5,127.5, 127.5])
        detections = net.forward()
        
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > min_confidence:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = CLASSES[idx]
                detected_objects.append(label)

                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 #if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        cv2.imshow("frame", frame)
        fps.update()
        key = cv2.waitKey(1) & 0xFF
        if (key == ord("q")) or (key == 27):
            quit = True
            break
        if (key == 0x20):
            while True:
                key = cv2.waitKey(1)
                if (key == 0x20):
                    break
                if (key == ord("q")) or (key == 27):
                    quit = True
                    break
            if quit:
                break
    if quit:
        break

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
