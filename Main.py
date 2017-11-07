import cv2
import numpy as np

# ------------------------------ Start of network tables ------------------------------

from networktables import NetworkTables

vision_table_name = "vision"


def nt_setup():
    NetworkTables.initialize()


vision_table = NetworkTables.getTable(vision_table_name)


def send_angle(value):
    vision_table.putNumber("angle", value)


def send_distance(value):
    vision_table.putNumber("distance", value)

# ------------------------------ End of network tables ------------------------------


hue, lum, sat = 0, 0, 0
hls = None
kernel = np.ones((5, 5), np.uint8)


def get_mouse_cords(event, xf, yf, flags, _):
    if event == cv2.EVENT_LBUTTONUP:
        huef = (hls[yf, xf, 0])
        lumf = (hls[yf, xf, 1])
        satf = (hls[yf, xf, 2])
        print(huef)
        print(lumf)
        print(satf)
        print('-')


def scorer(area, ratio):
    if area < 1000:  # make this value better
        return 0

    score_ = area / (((ratio - 8.5) ** 2) + 1)  # find the optimal ratio
    return score_


cv2.namedWindow('Original')
cv2.setMouseCallback('Original', get_mouse_cords)
cap = cv2.VideoCapture(2)

while True:
    _, img = cap.read()
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    img = cv2.bilateralFilter(img, 5, 75, 75)

    # Below are the actual values
    # lower1 = np.array([0, 170, 250])
    # upper1 = np.array([255, 255, 255])

    # these values below are only at home
    lower = np.array([80, 0, 0])
    upper = np.array([110, 255, 200])
    mask = cv2.inRange(hls, lower, upper)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('Opening', opening)

    cont = np.zeros(img.shape, np.uint8)
    _, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(cont, contours, -1, (0, 255, 0), 3)

    sized_contours = []
    good_sized_contours = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        ratio_ = h/w
        score = scorer(cv2.contourArea(c), ratio_)
        print("area: ", cv2.contourArea(c))
        print("ratio: ", ratio_)
        print("score: ", score)
        print("---------------")
        if score > 0:
            sized_contours.append(score)

    if sized_contours.__len__() > 1:
        sized_contours.sort()
        x, y, w, h = cv2.boundingRect(contours[(sized_contours.__len__() - 1)])
        x2, y2, w2, h2 = cv2.boundingRect(contours[(sized_contours.__len__() - 2)])
        cv2.rectangle(cont, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.rectangle(cont, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)

        x_end = 0
        if x2 >= x:
            x_end = (x2 + w2)
        elif x > x2:
            x_end = (x + w)
        y_end = 0
        if y2 >= y:
            y_end = (y2 + h2)
        elif y > y2:
            y_end = (y + h)

        x_start = 0
        if x2 <= x:
            x_start = x2
        elif x < x2:
            x_start = x

        y_start = 0
        if y2 <= y:
            y_start = y2
        elif y < y2:
            y_start = y

        x_center = ((x_end - x_start) / 2) + x_start
        y_center = ((y_end - y_start) / 2) + y_start

        cv2.rectangle(cont, (int(x_start), int(y_start)), (int(x_end), int(y_end)), (0, 0, 255), 2)

        cv2.circle(cont, (int(x_center), int(y_center)), 2, (0, 255, 0), 2)

        # get the values to put into here
        # send_angle()
        # send_distance()
        # --------------------------

    cv2.imshow('Original', img)
    cv2.imshow('contours', cont)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
