import numpy as np
import cv2
import time
from Keyinput import PressKey, FORWARD

start_nums = []
num = 0


def initStartNums():
    for num in range(1, 4):
        num_img = cv2.imread("data/start_{}.jpg".format(num), cv2.IMREAD_GRAYSCALE)
        _, num_img = cv2.threshold(num_img, 50, 255, cv2.THRESH_BINARY_INV)
        # cv2.imshow('img_{}'.format(num), num_img)
        start_nums.append(num_img)


def checkStart(img):
    global num
    if len(start_nums) == 0:
        initStartNums()
    roi = img[252:335, 480:545]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('roi', roi)
    for count, start_num in enumerate(start_nums):
        diff = cv2.bitwise_xor(roi, start_num)
        diff_cnt = cv2.countNonZero(diff)
        if diff_cnt < 20:
            print(count + 1)
            num = count + 1
            return count + 1
    if num == 1:
        print("START!")
        PressKey(FORWARD)
        return "Start"
    return 0
