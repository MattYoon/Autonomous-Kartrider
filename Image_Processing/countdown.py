import cv2
from keyinput import PressKey, ReleaseKey, FORWARD
import time


start_1 = None
def loadStart():
    global start_1
    num_img = cv2.imread("data/start_1.jpg", cv2.IMREAD_GRAYSCALE)
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
    if diff_cnt < 500:
        print("Ready")
        flag1 = True
        flag2 = False
        return False
    if flag1:
        if not flag2:
            flag2 = True
            return False
        else:
            print("Go!")
            PressKey(FORWARD)
            time.sleep(2)
            ReleaseKey(FORWARD)
            return True
    flag1 = False
    flag2 = False
    return False
