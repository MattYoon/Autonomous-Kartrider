import math

import keyinput


def distance_twopoint(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2))


def press_onekey(direction):
    if direction != 0:
        keyinput.PressKey(direction)
    # thread = threading.Thread(target=keyinput.PressKey, args=[direction])
    # thread.start()


def release_onekey(direction):
    if direction != 0:
        keyinput.ReleaseKey(direction)
    # thread = threading.Thread(target=keyinput.ReleaseKey, args=[direction])
    # thread.start()

def release_all():
    keyinput.ReleaseKey(keyinput.FORWARD)
    keyinput.ReleaseKey(keyinput.BACK)
    keyinput.ReleaseKey(keyinput.LEFT)
    keyinput.ReleaseKey(keyinput.RIGHT)


def get_player_detailed_pos(locations):
    """
    :param locations: 플레이어의 테두리를 이루는 점집합
    :return:
    """

    x = locations[0][0]
    y = locations[0][1]

    leftx = x
    leftpoint = locations[0]

    rightx = x
    rightpoint = locations[0]

    topy = y
    toppoint = locations[0]

    bottomy = y
    bottompoint = locations[0]

    for point in locations:
        if point[0] < leftx:
            leftx = point[0]
            leftpoint = point
        if point[0] > rightx:
            rightx = point[0]
            rightpoint = point
        if point[1] > topy:
            topy = point[1]
            toppoint = point
        if point[1] < bottomy:
            bottomy = point[1]
            bottompoint = point

    return leftpoint, rightpoint, toppoint, bottompoint

