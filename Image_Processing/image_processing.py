from Image_Processing.misc import getImg, calcFPS
from Image_Processing.countdown import loadStart, checkStart
from Image_Processing.minimap import getMinimapData
from Image_Processing.speed import loadSpeed, getSpeedData
from Image_Processing.reverse import isReverse
from reset_env import isReset, initReset, checkIFMenu
import cv2
import time as T
import threading


# 영상처리 main


def loadData():
    loadStart()
    loadSpeed()


def ipCountdown():
    print("Image Processing Running.. Waiting for Start Cue")
    while True:
        img = getImg()
        if img is None:
            break
        if checkStart(img):
            break
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            quit("Terminated by User")


def ipMain():
    global points, origin, player_vertex, speed, reverse
    #initGlobals()
    ipCountdown()
    while True:
        img = getImg()
        if img is None:
            break
        checkIFMenu(img[393:394, 437:438])
        minimap = img[217:319, 252:431]
        points, origin, player_vertex = getMinimapData(minimap)
        speed = getSpeedData(img)
        sign_area = img[257:261, 510:514]
        reverse = isReverse(sign_area)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            quit("Terminated by User")
        if isReset():
            cv2.destroyAllWindows()
            initReset()
            ipMain()


def initGlobals():
    global points, origin, player_vertex, speed, reverse
    points, origin, player_vertex, speed, reverse = None, None, None, None, None


# 아래의 모든 좌표는 튜플 (x, y) 형식

def getPoints():  # 파란점 4개
    global points
    return points  # (l1, r1, l2, r2)  l1 -> 왼쪽 위, r2 -> 오른쪽 아래


def getOrigin():   # 빨간점 1개
    global origin
    return origin


def getPlayerVertex():  # 초록점 1개
    global player_vertex
    return player_vertex


def getSpeed():
    global speed
    return speed  # int


def getReverse():  # 역주행인지 아닌지
    global reverse
    return reverse  # bool


points, origin, player_vertex, speed, reverse = None, None, None, None, None

time = T.time()
loadData()

thread = threading.Thread(target=ipMain)
thread.start()
T.sleep(0.1)