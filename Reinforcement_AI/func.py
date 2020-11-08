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
