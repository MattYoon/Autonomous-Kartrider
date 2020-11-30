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

    # print(len(locations))

    x = locations[0][0][0]
    y = locations[0][0][1]

    leftx = x
    leftpoint = locations[0][0]

    rightx = x
    rightpoint = locations[0][0]

    topy = y
    toppoint = locations[0][0]

    bottomy = y
    bottompoint = locations[0][0]

    for i in range(len(locations)):
        if locations[i][0][0] < leftx:
            leftx = locations[i][0][0]
            leftpoint = locations[i][0]
        if locations[i][0][0] > rightx:
            rightx = locations[i][0][0]
            rightpoint = locations[i][0]
        if locations[i][0][1] > topy:
            topy = locations[i][0][1]
            toppoint = locations[i][0]
        if locations[i][0][1] < bottomy:
            bottomy = locations[i][0][1]
            bottompoint = locations[i][0]

    return leftpoint, rightpoint, toppoint, bottompoint

