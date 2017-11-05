import cv2
import numpy as np

hue, lum, sat = 0, 0, 0
xd, yd = 0, 0
hls = None
kernel = np.ones((5, 5), np.uint8)


def get_mouse_coords(event, x, y, flags, _):
    if event == cv2.EVENT_LBUTTONUP:
        hue = (hls[y, x, 0])
        lum = (hls[y, x, 1])
        sat = (hls[y, x, 2])
        print(hue)
        print(lum)
        print(sat)
        print('-')


# def check_shape(c, mask)
#     area = cv2.contourArea(c)
#     if area < 2000:
#         return 0
#
#     x, y, w, h = cv2.boundingRect(c)
#
#     if not (0.5 < w / h < 0.65):
#         return 0
#
#     white_px = np.mean(mask[y:(y + h), x:(x + w)])
#     s = area / 15000 - (w / h - 0.57) ** 2 * 3000 + 4 * white_px / 255 + 100
#     # print(s, white_px)
#     return s

cv2.namedWindow('Original')
cv2.setMouseCallback('Original', get_mouse_coords)
cap = cv2.VideoCapture(2)

while True:
    _, img = cap.read()
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    img = cv2.bilateralFilter(img, 5, 75, 75)

    # Below are the actual values
    # lower1 = np.array([0, 170, 250])
    # upper1 = np.array([255, 255, 255])

    # these values below are only at home
    lower1 = np.array([80, 0, 0])
    upper1 = np.array([110, 255, 200])

    # lower2 = np.array([0, 0, 0])
    # upper2 = np.array([255, 255, 255])
    mask = cv2.inRange(hls, lower1, upper1)
    # mask2 = cv2.inRange(hls, lower2, upper2)
    # res = cv2.bitwise_or(mask, mask2)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # mask_copy = opening.copy()

    # bw_pic = cv2.cvtColor(opening, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(bw_pic, 127, 255, 0)

    cv2.imshow('Opening', opening)

    cont = np.zeros(img.shape, np.uint8)
    # opening = cv2.morphologyEx(cont, cv2.MORPH_OPEN, kernel)
    _, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(cont, contours, -1, (0, 255, 0), 3)

    sized_contours = []
    good_sized_contours = []

    for c in contours:
        sized_contours.append(cv2.contourArea(c))

    if sized_contours.__len__() > 1:
        sized_contours.sort()
        x, y, w, h = cv2.boundingRect(contours[(sized_contours.__len__() - 1)])
        x2, y2, w2, h2 = cv2.boundingRect(contours[(sized_contours.__len__() - 2)])
        cv2.rectangle(cont, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.rectangle(cont, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)

        x_width = 0
        # y_width = ((y + y2) / 2) + ((h + h2) / 2)
        if x2 > x:
            x_width = (x2 + w2)
        elif x > x2:
            x_width = (x + w)
        y_width = 0
        # y_width = ((y + y2) / 2) + ((h + h2) / 2)
        if y2 > y:
            y_width = (y2 + h2)
        elif y > y2:
            y_width = (y + h)

        x_start = 0
        if x2 < x:
            x_start = x2
        elif x < x2:
            x_start = x

        y_start = 0
        if y2 < y:
            y_start = y2
        elif y < y2:
            y_start = y

        x_center = ((x_width - x_start) / 2) + x_start
        y_center = ((y_width - y_start) / 2) + y_start

        cv2.rectangle(cont, (int(x_start), int(y_start)), (int(x_width), int(y_width)), (0, 0, 255), 2)

        cv2.circle(cont, (int(x_center), int(y_center)), 2, (0, 255, 0), 2)

    # good_contours = []
    # existing_contours = False
    # for c in contours:
    #     x, y, w, h = cv2.boundingRect(c)
    #     ratio = h/w
    #     if 8 < ratio < 14:
    #         good_contours.append(c)
    #         existing_contours = True
    #
    # if existing_contours == True:
    #     x, y, w, h = cv2.boundingRect(good_contours[0])
    #     if good_contours.__len__() > 1:
    #         x2, y2, w2, h2 = cv2.boundingRect(good_contours[1])
    #         cv2.rectangle(cont, (x, y), (x + w, y + h), (255, 255, 0), 2)
    #         cv2.rectangle(cont, (x2, y2), (x2 + w2, y2 + h2), (255, 255, 0), 2)
    #         x_center = 0
    #         y_center = 0
    #         x_center = (x + x2 + w)/2
    #         y_center = ((h + h2) / 4) + y
    #
    #         x_width = 0
    #         y_width = ((y + y2) / 2) + ((h + h2) / 2)
    #         if x2 > x:
    #             x_width = (x2 + w2)
    #         elif x > x2:
    #             x_width = (x + w)
    #
    #         x_start = 0
    #         y_start = (y + y2) / 2
    #         if x2 < x:
    #             x_start = x2
    #         elif x < x2:
    #             x_start = x
    #
    #         cv2.rectangle(cont, (x_start, int(y_start)), (int(x_width), int(y_width)), (0, 0, 255), 2)
    #
    #         cv2.circle(cont, (int(x_center), int(y_center)), 2, (0, 255, 0), 2)
    #         # print(x_center, " and ", y_center)
    #     else:
    #         cv2.rectangle(cont, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         # print("Only one column.")

    cv2.imshow('Original', img)
    cv2.imshow('contours', cont)
    # cv2.imshow('Mask', mask)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()