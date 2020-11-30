from time import sleep

import Reinforcement_AI.func as func
import keyinput
from Image_Processing.image_processing import getPlayerVertex, getOrigin, runIP, getSpeed, getPoints, getPlayerEdge
from reset_env import releaseAllKeys


def getXdiff():
        px, py = getPlayerVertex()  # 초록점
        ox, oy = getOrigin()  # 빨간점
        diff = px - ox  # 두 점의 x 좌표 차이
        # print("px-ox:", diff)
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

def drive_v2():
    diff = getXdiff()
    speed = getSpeed()
    points = getPoints()
    edge = getPlayerEdge()

    car_shifted = func.get_shifted(func.get_player_detailed_pos(edge[0], getPlayerVertex()))
    way_width = points[3][0] - points[2][0]

    # diff가 음수일땐 차가 좌측에 있을 때, diff가 양수일땐 차가 우측에 있을 때
    # diff가 음수면서, car_shifted가 양수면 (차가 좌측으로 휘어있으면), 우측으로 틀어야 함
    # diff가 양수면서, car_shifted가 음수면 (차가 우측으로 휘어있으면), 좌측으로 틀어야 함

    if speed < 100:
        speed_time_val = 1
    else:
        speed_time_val = 100 / speed

    # print(way_width * 0.2, diff)

    if diff < 0:    # 차가 좌측에 있을 때
        if car_shifted > 0:     # 만약 차가 좌측으로 휘어있으면:
            # if abs(diff) > way_width * 0.2:
            keyinput.PressAndRelease(keyinput.RIGHT, seconds=abs(diff * 0.01) / speed_time_val)
        else:                   # 이미 우측으로 휘어있으면?
            pass                # 방향전환 안함
    if diff > 0:    # 차가 우측에 있을 떄
        if car_shifted < 0:     # 만약 차가 우측으로 휘어있으면:
            # if abs(diff) > way_width * 0.2:
            keyinput.PressAndRelease(keyinput.LEFT, seconds=abs(diff * 0.01) / speed_time_val)
        else:
            pass




if __name__ == "__main__":
    from multiprocessing import Manager
    print("TRYING TO CREATE MANAGER")
    manager = Manager()
    print("CREATED MANAGER")
    runIP(manager)

    """version 1
    prev_diff = 0
    while True:
        sleep(0.001)
        prev_diff = drive(prev_diff)"""

    # version 2
    keyinput.PressKey(keyinput.FORWARD)
    while True:
        sleep(0.0001)
        drive_v2()