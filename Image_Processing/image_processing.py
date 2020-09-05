from Frame import Frame
from Countdown import checkStart
import cv2
import time as T

# 영상처리 main


def calcFPS(prevtime):
    global FPS
    curtime = T.time()
    latency = curtime - prevtime
    try:
        fps = 1/latency
        FPS.append(fps)
    except ZeroDivisionError:
        pass
    if len(FPS) == 50:
        print("FPS: %.0f" % (sum(FPS)/len(FPS)))
        FPS = []
    return curtime


frm = Frame()
time = T.time()
FPS = []

while True:
    time = calcFPS(time)
    img = frm.getImg()
    if img is None:
        break
    cv2.imshow('original', img)
    if checkStart(img) == "Start":
        break
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        quit("Terminated by User")

while True:
    time = calcFPS(time)
    img = frm.getImg()
    if img is None:
        break
    cv2.imshow('original', img)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        quit("Terminated by User")
