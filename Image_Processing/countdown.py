import os
import threading
import time

import cv2

from keyinput import PressAndRelease, FORWARD

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

start_1 = None
def loadStart():
    global start_1
    num_img = cv2.imread(BASE_DIR + "/data/start_1.jpg", cv2.IMREAD_GRAYSCALE)
    _, num_img = cv2.threshold(num_img, 50, 255, cv2.THRESH_BINARY_INV)
    start_1 = num_img


flag1 = False
flag2 = False  # for double check
def checkStart(img):
    global flag1, flag2, start_1
    roi = img[252:335, 480:545]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY_INV)
    diff = cv2.bitwise_xor(roi, start_1)
    diff_cnt = cv2.countNonZero(diff)
    if diff_cnt == 2:  # 왠지는 모르겠는데 내가 갖고 있는 데이터랑 실제 데이터랑 픽셀이 항상 2개 차이 남
        flag1 = True
        if not flag2:
            print("Ready")
            flag2 = True
            time.sleep(0.5)  # 왠지는 모르겠는데 sleep 없으면 가끔씩 제대로 작동 안함
        return False
    elif flag1:
        print("Go!")
        # PressAndRelease(FORWARD, 2)
        thread = threading.Thread(target=PressAndRelease, args=[FORWARD, 1.5])
        thread.start()
        # print("Please checkstart TT")
        time.sleep(1.5)
        flag1 = False
        flag2 = False
        return True
    flag1 = False
    flag2 = False
    return False
