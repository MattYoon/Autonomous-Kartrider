from Image_Processing.image_processing import getPlayerVertex, getOrigin, runIP
import keyinput
from reset_env import releaseAllKeys
from time import sleep


def getXdiff():
        px, py = getPlayerVertex()
        ox, oy = getOrigin()
        diff = px - ox
        print("px-ox:", diff)
        return diff

def drive(prev):
    diff = getXdiff()

    if prev * diff > 0:
        return diff
    else:
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