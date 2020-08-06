import numpy as np
import win32gui
from mss import mss

# 실행중인 카트라이더 프로그램 윈도우의 위치를 확인하고 해당 윈도우를 캡쳐 후 Numpy 배열로 전환


class Frame:
    img = None
    sct = mss()

    def __init__(self):
        self.initWinPos()

    def initWinPos(self):
        hwnd = win32gui.FindWindow(None, "KartRider Client")
        if hwnd == 0:
            self.img = None
            return False
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0] + 3
        y = rect[1] + 34
        win_pos = {'top': y, 'left': x, 'width': 1024, 'height': 760}
        sct_img = self.sct.grab(win_pos)
        self.img = np.array(sct_img)
        return True

    def getImg(self):
        self.initWinPos()
        if self.img is not None:
            #cv2.imshow('original', self.img)
            return self.img
        else:
            print("Please run Kartrider")
            return None


if __name__ == "__main__":
    frm = Frame()

    while True:
        img = frm.getImg()
        if img is None:
            break
        else:
            print(img)
