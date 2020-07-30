import cv2
import numpy as np
import scipy
from scipy import ndimage, misc

def nothing(x):
    pass
cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

frame_counter=0
currect_pixel_sum=0
percent_square=0.75
total_pixels_square=3767880;

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    #lower_blue = np.array([0, 188, 83])
    #upper_blue = np.array([9, 227, 188])
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    scipy.ndimage.median_filter(mask, size=10, footprint=None, output=mask2, mode='reflect', cval=0.0, origin=0)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("mask2", mask2)
    cv2.imshow("result", result)
    key = cv2.waitKey(1)
    if key == 27: #esc key
        break
    if frame_counter>=13:
        frame_counter=0
        currect_pixel_sum= mask2.sum()
        if (currect_pixel_sum>=percent_square*total_pixels_square):
            print("succeed")
        else:
            print("fail")

    else:
        frame_counter=frame_counter+1
cap.release()
cv2.destroyAllWindows()
