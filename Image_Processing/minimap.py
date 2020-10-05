import numpy as np
import cv2
from Image_Processing import minimap_handler as mh


BOUND1 = np.array([0, 0, 170])
BOUND2 = np.array([255, 255, 255])
def getPathData(map_up):
    global map_warped
    map_hsv = cv2.cvtColor(map_up, cv2.COLOR_BGR2HSV)
    v_mask = cv2.inRange(map_hsv, BOUND1, BOUND2)
    map_valued = cv2.bitwise_and(map_up, map_up, mask=v_mask)
    map_gray = cv2.cvtColor(map_valued, cv2.COLOR_BGR2GRAY)
    map_blurred = cv2.GaussianBlur(map_gray, (21, 21), 0)
    _, map_thr = cv2.threshold(map_blurred, 145, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(map_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    points = mh.getPoints(contours)  # (l1, r1, l2, r2)
    for point in points:
        cv2.circle(map_warped, point, 5, (255, 0, 0), 2)
    origin = mh.calcOrigin(contours)
    cv2.circle(map_warped, origin, 5, (0, 0, 255), 2)
    return points, origin


VALUE1 = np.array([2, 190, 130])
VALUE2 = np.array([7, 255, 230])
prev_con = None
def getPlayerData(map_down):
    global map_warped, prev_con
    map_hsv = cv2.cvtColor(map_down, cv2.COLOR_BGR2HSV)
    v_mask = cv2.inRange(map_hsv, VALUE1, VALUE2)
    map_valued = cv2.bitwise_and(map_down, map_down, mask=v_mask)
    map_gray = cv2.cvtColor(map_valued, cv2.COLOR_BGR2GRAY)
    map_blurred = cv2.GaussianBlur(map_gray, (3, 3), 0)
    _, map_thr = cv2.threshold(map_blurred, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(map_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    vertex = mh.getVertex(contours)
    cv2.circle(map_warped, vertex, 5, (0, 255, 0), 2)
    try:
        for entry in contours[0]:
            entry[0][1] += 54  # shift the contour down to the right position
        prev_con = contours
        return contours, vertex
    except IndexError:
        return prev_con, vertex


map_warped = None
MATRIX = [[9.1871, 7.2361, -738.0782], [0.0035, 15.6320, -658.0158], [-0.0000, 0.0802, 1.0000]]
def getMinimapData(minimap):
    global map_warped
    simple_map = np.full_like(minimap, 255)
    map_warped = cv2.warpPerspective(minimap, np.float32(MATRIX), (minimap.shape[1], minimap.shape[0]))
    points, origin = getPathData(map_warped[:54])
    player_con, vertex = getPlayerData(map_warped[54:])
    cv2.imshow('minimap', map_warped)
    # cv2.line(simple_map, points[0], points[1], (255, 0, 0), 4)
    # cv2.line(simple_map, points[0], points[2], (255, 0, 0), 4)
    # cv2.line(simple_map, points[1], points[3], (255, 0, 0), 4)
    # cv2.line(simple_map, points[2], points[3], (255, 0, 0), 4)

    points_arr = np.array([points[0], points[2], points[3], points[1]])
    #4646cv2.polylines(simple_map, [points_arr], True, (255, 0, 0), 10)
    cv2.fillPoly(simple_map, [points_arr], (255, 0, 0))
    cv2.drawContours(simple_map, player_con, 0, (0, 0, 255), -1)
    cv2.imshow('simple_map', simple_map)
    return points, origin, vertex, simple_map
