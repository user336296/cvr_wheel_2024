import numpy as np
import cv2
import math
cv2.namedWindow("mask")

def nothing(x):
    pass
low_hsv = (1, 82, 172)
high_hsv = (217, 157, 218)

lh, ls, lv = low_hsv
hh, hs, hv = high_hsv

cv2.createTrackbar("lh", "mask", lh, 255, nothing)
cv2.createTrackbar("ls", "mask", ls, 255, nothing)
cv2.createTrackbar("lv", "mask", lv, 255, nothing)
cv2.createTrackbar("hh", "mask", hh, 255, nothing)
cv2.createTrackbar("hs", "mask", hs, 255, nothing)
cv2.createTrackbar("hv", "mask", hv, 255, nothing)

calibration_distance = 100 # см
calibration_linear_size = 61 # pixel
# cam = cv2.VideoCapture(1)
# hsv  (1, 82, 172) (217, 157, 218)
while (True):
    # success, frame = cam.read()
    frame = cv2.imread('ball_unknown_distance.jpg')
    #frame[100 : 550, 100 : 550, 0] = 240
    #frame[:, :, 2] += 50
    
    #print(frame.shape)
    
    #frame = 255 - frame

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lh = cv2.getTrackbarPos("lh", "mask")
    ls = cv2.getTrackbarPos("ls", "mask")
    lv = cv2.getTrackbarPos("lv", "mask")
    hh = cv2.getTrackbarPos("hh", "mask")
    hs = cv2.getTrackbarPos("hs", "mask")
    hv = cv2.getTrackbarPos("hv", "mask")
    
    mask = cv2.inRange(hsv, (lh, ls, lv), (hh, hs, hv))
    print((lh, ls, lv), (hh, hs, hv))
    cv2.imshow("mask", mask)
    
    connectivity = 4
    # Perform the operation
    output = cv2.connectedComponentsWithStats(mask, connectivity, cv2.CV_32S)
    
    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]
    # The second cell is the label matrix
    labels = output[1]
    # The third cell is the stat matrix
    stats = output[2]
    
    filtered = np.zeros_like(mask)
    
    for i in range(1, num_labels):
        a = stats[i, cv2.CC_STAT_AREA]
        t = stats[i, cv2.CC_STAT_TOP]
        l = stats[i, cv2.CC_STAT_LEFT]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        
        #print(a)
        
        if (a >= 1000):
            filtered[np.where(labels == i)] = 255
            #print(a)
            linear_size = math.sqrt(a)

            distance_by_cam = round(calibration_distance * calibration_linear_size / linear_size)
            cv2.putText(frame, str(distance_by_cam), (l + w + 10, t + h + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(a), (l, t), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (l, t), (l + w, t + h), (0, 255, 0), 2)
        
    #print("=====================")
    #break
    
    cv2.imshow("frame", frame)
    #cv2.imshow("hsv", hsv[:, :, 0])
    cv2.imshow("filtered", filtered)
    
    key = cv2.waitKey(280) & 0xFF
    
    if (key == ord(' ')):
        break

# cam.release()
cv2.destroyAllWindows()
cv2.waitKey(10)
