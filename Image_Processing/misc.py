import numpy as np
import win32gui
from mss import mss
import cv2
import time as T
import glob
import os


# 실행중인 카트라이더 프로그램 윈도우의 위치를 확인하고 해당 윈도우를 캡쳐 후 Numpy 배열로 전환
def getImg():
    sct = mss()
    hwnd = win32gui.FindWindow(None, "KartRider Client")
    if hwnd == 0:
        quit("Please run KartRider")
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0] + 3
    y = rect[1] + 34
    win_pos = {'top': y, 'left': x, 'width': 1024, 'height': 760}
    sct_img = sct.grab(win_pos)
    img = np.array(sct_img)
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


FPS = []
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


def rmRider(): # 쉐도우 플레이어? 쨌든 그거 제거
    path = 'C:/Users/Yoon/Documents/카트라이더/라이더데이터'
    print(os.path.exists(path))
    if os.path.exists(path):
        files = glob.glob(path + '/*')
        for f in files:
            os.remove(f)
        global file
        T.sleep(3)
    else:
        quit("misc.py rmRider()의 path 변수를 알맞게 수정해주세요")