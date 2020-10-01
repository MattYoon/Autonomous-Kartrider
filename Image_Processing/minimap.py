import numpy as np
import cv2

map_warped = None


def divideCont(contours):
    left = []
    right = []
    flag = False
    for y in range(53, 0, -1):
        try:
            tmp = contours[0][np.where(contours[0][:, 0, 1] == y)]
            x_values = []
            for entry in tmp:
                if entry[0][0] == 178:
                    flag = True
                x_values.append(entry[0][0])
            if len(x_values) > 0:
                if not flag:
                    x_values.sort()
                    left.append([x_values[0], y])
                    right.append([x_values[-1], y])
                elif flag:
                    x_values.sort()
                    left.append([x_values[0], y])
        except IndexError:
            pass
    return left, right


def calcOrigin(contours):
    x = -1
    y = 53
    while y >= 50:
        try:
            bottoms = contours[0][np.where(contours[0][:, 0, 1] == y)]
            bottoms[0][0, 1]
            x = int(round(np.mean(bottoms[:, 0, 0]), 0))
            break
        except IndexError:
            y -= 1
    return [x, y]


def checkHorizontal(shifted_half, other_half, origin):
    if shifted_half[-1][0] < origin[0]:
        return True
    elif (other_half[-1][0] < shifted_half[-1][0]) and abs(other_half[-1][1] - shifted_half[-1][1]) < 3:
        return True
    return False


def checkShort(half_cont):
    coor1 = np.array(half_cont[0])
    coor2 = np.array(half_cont[-1])
    dist = np.linalg.norm(coor2 - coor1)
    if dist < 50:
        return True
    return False


def checkInvalid(half_cont, track, other_half, origin):
    if len(track) < 5:
        return True
    elif checkHorizontal(track, other_half, origin):
        return True
    elif checkShort(half_cont):
        return True
    elif origin[0] < 20 or origin[0] > 159:
        return True
    else:
        return False


def averageBoth(left_cont, right_cont):
    track = []
    left = np.array(left_cont)
    right = np.array(right_cont)
    for y in range(53, 0, -1):
        left_coor = left[np.where(left[:, 1] == y)]
        right_coor = right[np.where(right[:, 1] == y)]
        try:
            x_avg = (left_coor[0][0] + right_coor[0][0])//2
            track.append([x_avg, y])
        except IndexError:
            break
    return track


def shiftLeft(origin, left_con):
    shifted = []
    shift = origin[0] - left_con[0][0]
    for coor in left_con:
        shifted.append([coor[0] + shift, coor[1]])
    return shifted


def get_track(left_cont, right_cont, origin):
    if len(left_cont) - len(right_cont) < 5:
        return averageBoth(left_cont, right_cont)
    else:
        return shiftLeft(origin, left_cont)


bound1 = np.array([0, 0, 170])
bound2 = np.array([255, 255, 255])
prev_origin = []
prev_track = []
prev_con = []
def getPathData(map_up):
    global prev_origin, prev_track, prev_con, map_warped
    map_hsv = cv2.cvtColor(map_up, cv2.COLOR_BGR2HSV)
    v_mask = cv2.inRange(map_hsv, bound1, bound2)
    map_valued = cv2.bitwise_and(map_up, map_up, mask=v_mask)
    map_gray = cv2.cvtColor(map_valued, cv2.COLOR_BGR2GRAY)
    map_blurred = cv2.GaussianBlur(map_gray, (21, 21), 0)
    _, map_thr = cv2.threshold(map_blurred, 145, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(map_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(map_warped, contours, -1, (0, 255, 0), 1)

    try:
        left_con, right_con = divideCont(contours)
        origin = calcOrigin(contours)
        track = get_track(left_con, right_con, origin)
        if checkInvalid(left_con, track, right_con, origin):
            origin = prev_origin
            track = prev_track
        prev_origin = origin
        prev_track = track
        prev_con = contours

    except IndexError:
        origin = prev_origin
        track = prev_track
        contours = prev_con
        prev_origin = origin
        prev_track = track
        prev_con = contours

    if (len(origin) > 0) and (len(track) > 0):
        cv2.circle(map_warped, (origin[0], origin[1]), 4, (255, 255, 0), -1)
        for point in track:
            cv2.circle(map_warped, (point[0], point[1]), 2, (0, 0, 255), -1)

    return origin, track, contours[0]


value1 = np.array([2, 190, 130])
value2 = np.array([7, 255, 230])


def getPlayerData(map_down):
    global map_warped
    map_hsv = cv2.cvtColor(map_down, cv2.COLOR_BGR2HSV)
    v_mask = cv2.inRange(map_hsv, value1, value2)
    map_valued = cv2.bitwise_and(map_down, map_down, mask=v_mask)
    map_gray = cv2.cvtColor(map_valued, cv2.COLOR_BGR2GRAY)
    map_blurred = cv2.GaussianBlur(map_gray, (3, 3), 0)
    _, map_thr = cv2.threshold(map_blurred, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(map_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        for cont in contours[0]:
            cont[0][1] += 54
        cv2.drawContours(map_warped, contours, -1, (0, 255, 0), 2)
        return contours[0]
    except IndexError:
        return None


matrix = [[9.1871, 7.2361, -738.0782], [0.0035, 15.6320, -658.0158], [-0.0000, 0.0802, 1.0000]]
def getMinimapData(minimap):
    global map_warped
    map_warped = cv2.warpPerspective(minimap, np.float32(matrix), (minimap.shape[1], minimap.shape[0]))
    origin, track, track_con = getPathData(map_warped[:54])
    player_con = getPlayerData(map_warped[54:])
    cv2.imshow('minimap', map_warped)
    return origin, track, track_con, player_con
