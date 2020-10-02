import cv2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



speed_nums = []
def loadSpeed():
    global speed_nums
    for i in range(10):
        path = BASE_DIR + f'/data/speed_{i}.jpg'
        num = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        _, num_thresh = cv2.threshold(num, 150, 255, cv2.THRESH_BINARY)
        speed_nums.append(num_thresh)


def matchNum(img):
    global speed_nums
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    for i, speed_num in enumerate(speed_nums):
        diff = cv2.bitwise_xor(img_thresh, speed_num)
        diff_cnt = cv2.countNonZero(diff)
        if diff_cnt < 30:
            return i
    return 0


def getSpeedData(img):
    nx = img[690:730, 489:511]  # 두자리 수 첫자리
    nxx = img[690:730, 478:500]  # 세자리 수 첫자리
    xnx = img[690:730, 500:522]  # 세자리 수 둘째자리

    nx_num = matchNum(nx)
    nxx_num = matchNum(nxx)
    xnx_num = matchNum(xnx)
    final_speed = 0
    final_speed += nx_num * 10
    final_speed += xnx_num * 10
    final_speed += nxx_num * 100
    return final_speed
