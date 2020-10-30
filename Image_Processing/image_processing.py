from Image_Processing.misc import getImg
from Image_Processing.countdown import loadStart, checkStart
from Image_Processing.minimap import getMinimapData
from Image_Processing.minimap_handler import resetValues
from Image_Processing.speed import loadSpeed, getSpeedData
from Image_Processing.reverse import isReverse
from reset_env import isReset, initReset, checkIFMenu
import cv2
import time as T
import multiprocessing

# 영상처리 main


def loadData():
    loadStart()
    loadSpeed()


def ipCountdown():
    print("Image Processing Running.. Waiting for Start Cue")
    while True:
        img = getImg()
        if img is None:
            print("None")
            break
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
        resetData()
        while True:
            img = getImg()
            if img is None:
                break
            checkIFMenu(img[393:394, 437:438])
            minimap = img[217:319, 252:431]
            d['points'], d['origin'], d['player_vertex'], d['simple_map'] = getMinimapData(minimap)
            d['speed'] = getSpeedData(img)
            sign_area = img[257:261, 510:514]
            d['reverse'] = isReverse(sign_area)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                quit("Terminated by User")
            if isReset():
                cv2.destroyAllWindows()
                initReset()
                resetValues()
                #releaseAllKeys()
                break


def resetData():
    global shared_dict
    shared_dict['points'] = (35, 0), (146, 0), (33, 53), (147, 53)
    shared_dict['origin'] = (90, 53)
    shared_dict['player_vertex'] = (89, 55)
    shared_dict['speed'] = None
    shared_dict['reverse'] = False
    shared_dict['simple_map'] = None


# 아래의 모든 좌표는 튜플 (x, y) 형식

def getPoints():  # 파란점 4개
    return shared_dict['points']  # (l1, r1, l2, r2)  l1 -> 왼쪽 위, r2 -> 오른쪽 아래


def getOrigin():   # 빨간점 1개
    return shared_dict['origin']


def getPlayerVertex():  # 초록점 1개
    return shared_dict['player_vertex']


def getSpeed():
    return shared_dict['speed']  # int


def getReverse():  # 역주행인지 아닌지
    return shared_dict['reverse']  # bool


def getSimpleMap():
    return shared_dict['simple_map']  # (102, 179, 3) numpy array
    # 102 -> y축, 179 -> x축, 3 -> BGR
    # (255, 255, 255) -> white, (255, 0, 0) -> blue, (0, 0, 255) -> red


shared_dict = {}
loadData()
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


# if __name__ == "__main__":
#     from multiprocessing import Manager
#     print("TRYING TO CREATE MANAGER")
#     manager = Manager()
#     print("CREATED MANAGER")
#     runIP(manager)
#     while True:
#         print("현재 속도:", shared_dict['speed'])
#         T.sleep(1)

