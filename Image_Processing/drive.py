from Image_Processing.image_processing import getPlayerVertex, getOrigin, runIP
import keyinput
from reset_env import releaseAllKeys
from time import sleep


def getXdiff():
        px, py = getPlayerVertex()  # 초록점
        ox, oy = getOrigin()  # 빨간점
        diff = px - ox  # 두 점의 x 좌표 차이
        print("px-ox:", diff)
        return diff

def drive(prev):
    diff = getXdiff()

    if prev * diff > 0:  # diff와 prev의 부호가 같은 경우, 즉 계속 같은 방향으로 회전하면 되는 경우
        return diff  # 기존 방향으로 계속 회전
    else:  # 방향을 바꿔야 되는 경우
        releaseAllKeys()

    if diff < 0:
        keyinput.PressKey(keyinput.FORWARD)
        keyinput.PressKey(keyinput.RIGHT)
    elif diff > 0:
        keyinput.PressKey(keyinput.FORWARD)
        keyinput.PressKey(keyinput.LEFT)
    else:
        keyinput.PressKey(keyinput.FORWARD)
    return diff


if __name__ == "__main__":
    from multiprocessing import Manager
    print("TRYING TO CREATE MANAGER")
    manager = Manager()
    print("CREATED MANAGER")
    runIP(manager)
    prev_diff = 0
    while True:
        sleep(0.001)
        prev_diff = drive(prev_diff)