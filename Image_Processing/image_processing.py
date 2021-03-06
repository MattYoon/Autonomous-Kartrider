from Image_Processing.misc import getImg
from Image_Processing.countdown import loadStart, checkStart
from Image_Processing.minimap import getMinimapData
from Image_Processing.minimap_handler import resetValues
from Image_Processing.speed import loadSpeed, getSpeedData
from Image_Processing.extra import isReverse, loadLap, checkLap, isBoost
from reset_env import isReset, initReset, checkIFMenu
import cv2
import time as T
import multiprocessing
import numpy as np


# 영상처리 main


def loadData():
    loadStart()
    loadSpeed()
    loadLap()


def ipCountdown():
    print("Image Processing Running.. Waiting for Start Cue")
    while True:
        img = getImg()
        if img is None:
            print("None")
            break
        resetData()
        if checkStart(img):
            print("Checkstart")
            break
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            quit("Terminated by User")


def ipMain(d):
    print("Child: Created")
    while True:
        while True:
            img = getImg()
            if img is None:
                break
            checkIFMenu(img[393:394, 437:438])
            minimap = img[217:319, 252:431]
            d['points'], d['origin'], d['origin2'], d['player_edge'], d['player_vertex'], d['simple_map_pre'] = getMinimapData(minimap)
            d['speed'] = getSpeedData(img)
            drawSpeedGauge(d)
            sign_area = img[257:261, 510:514]
            d['reverse'] = isReverse(sign_area)
            lap_area = img[21:79, 923:972]
            d['lap2'] = checkLap(lap_area)
            boost_area = img[8:66, 101:159]
            d['boost'] = isBoost(boost_area)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                quit("Terminated by User")
            if isReset():
                cv2.destroyAllWindows()
                initReset()
                resetValues()
                # releaseAllKeys()
                break


BUFFER = np.full((40, 179, 3), 255, dtype=np.uint8)


def drawSpeedGauge(d):
    global simple_map
    speed_norm = d['speed'] / 250
    speed_scaled = int(speed_norm * 179)  # 기존 simple_map 가로 길이에 맞게 정규화
    simple_map = d['simple_map_pre']
    simple_map = np.vstack((simple_map, BUFFER))  # 기존 simple_map 아래에 흰색 여백 추가
    cv2.line(simple_map, (0, 120), (speed_scaled, 120), (0, 255, 0), 10)
    cv2.imshow('simple_map', simple_map)
    d['simple_map'] = simple_map


def resetData():
    global shared_dict
    shared_dict['points'] = (35, 0), (146, 0), (33, 53), (147, 53)
    shared_dict['origin'] = (90, 53)
    shared_dict['origin2'] = (90, 0)
    shared_dict['player_edge'] = None
    shared_dict['player_vertex'] = (89, 55)
    shared_dict['speed'] = 0
    shared_dict['reverse'] = False
    shared_dict['simple_map'] = 0
    shared_dict['lap2'] = False
    shared_dict['boost'] = False


# 아래의 모든 좌표는 튜플 (x, y) 형식

def getPoints():  # 파란점 4개
    return shared_dict['points']  # (l1, r1, l2, r2)  l1 -> 왼쪽 위, r2 -> 오른쪽 아래


def getOrigin():  # 빨간점 1개
    return shared_dict['origin']


def getOrigin2():
    return shared_dict['origin2']


def getPlayerEdge():  # 플레이어 아이콘 테두리
    return shared_dict['player_edge']


def getPlayerVertex():  # 초록점 1개
    return shared_dict['player_vertex']


def getSpeed():
    return shared_dict['speed']  # int


def getReverse():  # 역주행인지 아닌지
    return shared_dict['reverse']  # bool


def getSimpleMap():
    return shared_dict['simple_map']  # (142, 179, 3) numpy array
    # 142 -> y축, 179 -> x축, 3 -> BGR
    # (255, 255, 255) -> white, (255, 0, 0) -> blue, (0, 255, 0) -> green (0, 0, 255) -> red


def isLap2():  # lap2가 되면 True로 변경됨
    return shared_dict['lap2']  # bool


def getBoost():  # booster가 있으면 True
    return shared_dict['boost']  # bool


loadData()
shared_dict = {}


# simple_map = None
def runIP(manager):
    global shared_dict
    print("IMAGE PROCESSING")
    getImg()
    shared_dict = manager.dict()
    print("Parent: Creating Child")
    process = multiprocessing.Process(target=ipMain, args=[shared_dict])
    process.start()
    T.sleep(2)
    print("IMAGE PROCESSING END")


if __name__ == "__main__":
    from multiprocessing import Manager

    print("TRYING TO CREATE MANAGER")
    manager = Manager()
    print("CREATED MANAGER")
    runIP(manager)
    while True:
        pass
