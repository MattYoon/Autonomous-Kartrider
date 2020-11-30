import cv2
import numpy as np
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VALUE1 = np.array([0, 220, 200])
VALUE2 = np.array([0, 255, 255])
def isReverse(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v_mask = cv2.inRange(img_hsv, VALUE1, VALUE2)
    img_masked = cv2.bitwise_and(img, img, mask=v_mask)
    img_masked_gray = cv2.cvtColor(img_masked, cv2.COLOR_BGR2GRAY)
    _, sign_thresh = cv2.threshold(img_masked_gray, 50, 255, cv2.THRESH_BINARY)
    diff_cnt = cv2.countNonZero(sign_thresh)
    if diff_cnt:
        return True
    return False


prev_roi = None
def isBoost(roi):
    global prev_roi

    roi_gr = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi_bin = cv2.threshold(roi_gr, 170, 255, cv2.THRESH_BINARY)

    if prev_roi is not None:
        diff = cv2.bitwise_and(roi_bin, prev_roi)
        diff_cnt = cv2.countNonZero(diff)
        prev_roi = roi_bin
        if diff_cnt > 300:
            return True
        else:
            return False
    prev_roi = roi_bin
    return False


LAP2 = None
def loadLap():
    global LAP2
    lap2 = cv2.imread(BASE_DIR + '/data/lap2.jpg', cv2.IMREAD_GRAYSCALE)
    _, LAP2 = cv2.threshold(lap2, 175, 255, cv2.THRESH_BINARY)

def checkLap(img):
    global LAP2
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thr = cv2.threshold(img_gray, 175, 255, cv2.THRESH_BINARY)
    #cv2.imshow('lap', img_thr)
    diff = cv2.bitwise_xor(img_thr, LAP2)
    diff_cnt = cv2.countNonZero(diff)
    if diff_cnt < 50:
        return True
    return False


