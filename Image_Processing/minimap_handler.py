import numpy as np
from math import sqrt


prev_l1, prev_r1 = (35, 0), (146, 0)
def getL1R1(contours):
    global prev_l1, prev_r1
    try:
        top_edge = contours[0][np.where(contours[0][:, 0, 1] == 0)]
        right_edge = contours[0][np.where(contours[0][:, 0, 0] == 178)]
        if top_edge.shape[0] > 0 and right_edge.shape[0] > 0:  # right turn
            l1, r1 = hor1ver1Points(top_edge, right_edge, 0, 178)
        elif top_edge.shape[0] > 0:  # straight
            l1, r1 = hor2Points(top_edge, 0)
        elif right_edge.shape[0] > 0:  # hard right
            l1, r1 = ver2Points(right_edge, 178)
        else:  # something wrong
            return prev_l1, prev_r1
    except IndexError:
        return prev_l1, prev_r1
    dist = calcDist(l1, r1)
    if dist < 15 or dist > 95:
        return prev_l1, prev_r1
    prev_l1, prev_r1 = l1, r1
    return l1, r1


prev_l2, prev_r2 = (33, 53), (147, 53)
def getL2R2(contours):
    global prev_l2, prev_r2
    try:
        bottom_edge = contours[0][np.where(contours[0][:, 0, 1] == 53)]
        l2, r2 = hor2Points(bottom_edge, 53)
    except IndexError:
        return prev_l2, prev_r2
    dist = calcDist(l2, r2)
    if dist < 15 or dist > 95:
        return prev_l2, prev_r2
    prev_l2, prev_r2 = l2, r2
    return l2, r2


def getPoints(contours):
    l1, r1 = getL1R1(contours)
    l2, r2 = getL2R2(contours)
    points = (l1, r1, l2, r2)
    return points


prev_origin = (90, 53)
def calcOrigin(contours):
    global prev_origin
    try:
        bottom_edge = contours[0][np.where(contours[0][:, 0, 1] == 53)]
        x_values = [entry[0][0] for entry in bottom_edge]
        x_values.sort()
        medium = int(len(x_values)/2)
        origin = (x_values[medium], 53)
    except IndexError:
        return prev_origin
    except ValueError:
        return prev_origin
    prev_origin = origin
    return origin


prev_vertex = (89, 55)
def getVertex(contours):
    global prev_vertex
    try:
        vertex = contours[0][0][0]
        vertex[1] += 54
    except IndexError:
        return prev_vertex
    if calcDist(prev_vertex, vertex) > 7:
        return prev_vertex
    prev_vertex = tuple(vertex)
    return tuple(vertex)


def hor2Points(hor_edge, y):
    x_values = [entry[0][0] for entry in hor_edge]
    x_values.sort()
    q1, q3 = getQuartile(x_values)
    return (q1, y), (q3, y)


def ver2Points(ver_edge, x):
    y_values = [entry[0][1] for entry in ver_edge]
    y_values.sort()
    q1, q3 = getQuartile(y_values)
    return (x, q1), (x, q3)


def hor1ver1Points(hor_edge, ver_edge, y, x):
    x_values = [entry[0][0] for entry in hor_edge]
    x_values.sort()
    y_values = [entry[0][1] for entry in ver_edge]
    y_values.sort()
    x_q1, _ = getQuartile(x_values)
    _, y_q3 = getQuartile(y_values)
    return (x_q1, y), (x, y_q3)


def getQuartile(data):
    length = len(data)
    q1 = int(length*0.10)
    q3 = int(length*0.90)
    return data[q1], data[q3]


def calcDist(point1, point2):
    dist = sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return dist


