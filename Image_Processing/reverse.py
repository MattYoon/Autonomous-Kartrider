import cv2
import numpy as np


value1 = np.array([0, 220, 200])
value2 = np.array([0, 255, 255])
def isReverse(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v_mask = cv2.inRange(img_hsv, value1, value2)
    img_masked = cv2.bitwise_and(img, img, mask=v_mask)
    img_masked_gray = cv2.cvtColor(img_masked, cv2.COLOR_BGR2GRAY)
    _, sign_thresh = cv2.threshold(img_masked_gray, 50, 255, cv2.THRESH_BINARY)
    diff_cnt = cv2.countNonZero(sign_thresh)
    if diff_cnt:
        return True
    return False

