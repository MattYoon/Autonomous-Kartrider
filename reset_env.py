import autoit
from Image_Processing.misc import getWinPos
from keyinput import PressAndRelease, ReleaseKey, FORWARD, RIGHT, LEFT, BACK, ESCAPE
import numpy as np
import time


START_X = 432
START_Y = 398
RESET_X = 456
RESET_Y = 370


reset_flag = False


def checkIFMenu(sample_pix):
    if (sample_pix[0, 0] == np.array([72, 73, 192])).all():  # 메뉴에서 시작버튼 색
        print("in menu")
        startFromMenu()
        return True
    return False


def startFromMenu():  # 게임이 종료되고 메뉴로 나가진 상황에서 다시 시작
    global reset_flag
    win_pos = getWinPos()
    x = win_pos['left']
    y = win_pos['top']
    autoit.mouse_click("left", x + START_X, y + START_Y, 1)
    reset_flag = True


def manualReset():  # 게임 중 reset
    global reset_flag
    print("manual reset")
    PressAndRelease(ESCAPE, 0.1)
    win_pos = getWinPos()
    x = win_pos['left']
    y = win_pos['top']
    autoit.mouse_click("left", x + RESET_X, y + RESET_Y, 1)
    reset_flag = True


def releaseAllKeys():
    ReleaseKey(FORWARD)
    ReleaseKey(RIGHT)
    ReleaseKey(LEFT)
    ReleaseKey(BACK)


def isReset():
    global reset_flag
    return reset_flag


def initReset():
    global reset_flag
    reset_flag = False