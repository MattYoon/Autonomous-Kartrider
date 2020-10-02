from Image_Processing.misc import getImg, calcFPS
from Image_Processing.countdown import loadStart, checkStart
from Image_Processing.minimap import getMinimapData
from Image_Processing.speed import loadSpeed, getSpeedData
from Image_Processing.reverse import isReverse
import cv2
import time as T
import threading

# 영상처리 main


def loadData():
    loadStart()
    loadSpeed()


def ipCountdown():
    global time
    while True:
        #time = calcFPS(time)
        img = getImg()
        if img is None:
            break
        if checkStart(img):
            break
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            quit("Terminated by User")


def ipMain():
    global origin, track, track_con, player_con, time, speed
    while True:
        #time = calcFPS(time)
        img = getImg()
        if img is None:
            break
        minimap = img[217:319, 252:431]
        origin, track, track_con, player_con = getMinimapData(minimap)
        speed = getSpeedData(img)
        sign_area = img[257:261, 510:514]
        isReverse(sign_area)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            quit("Terminated by User")


def getOrigin(): #파란점
    global origin
    return origin


def getTrack(): #빨간선
    global track
    return track


def getTrackCon(): #트랙 주변 얇은 초록선
    global track_con
    return track_con


def getPlayerCon(): #플레이어 아이콘 초록
    global player_con
    return player_con


def getSpeed(): # 속도 10단위
    global speed
    return speed


def getReverse(): # 역주행인지 아닌지
    global reverse
    return reverse


origin, track, track_con, player_con, speed, reverse = None, None, None, None, None, None

time = T.time()
loadData()

print("Image Processing Running.. Waiting for Start Cue")
ipCountdown()
thread = threading.Thread(target=ipMain)
thread.start()
T.sleep(0.1)