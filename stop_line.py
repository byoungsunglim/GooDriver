import cv2
import numpy as np
import time
import math

def stop_line(ip_cam):
    y_pos = 0
    cap = cv2.VideoCapture(ip_cam)

    # while(cap.isOpened()):
    ret, frame = cap.read()

    if(ret):
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # #white
        # mask0 = cv2.inRange(hsv, (0,0,180), (180,38,255))

        # ## Merge the mask and crop the red regions
        # imgThreshHigh_white = cv2.bitwise_and(frame, frame, mask=mask0)

        # thresh_white = cv2.medianBlur(imgThreshHigh_white,5)
        # thresh_white = cv2.threshold(thresh_white, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

        # thresh_white = cv2.erode(thresh_white, None, iterations=2)
        # thresh_white = cv2.dilate(thresh_white, None, iterations=4)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv, (0,0,180), (180,38,255))

        imgThreshHigh_white = cv2.bitwise_and(frame, frame, mask=mask0)
        thresh_white = cv2.threshold(imgThreshHigh_white, 150, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

        gray = cv2.cvtColor(thresh_white,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,30,150,apertureSize = 3)

        lines = cv2.HoughLines(edges,1,np.pi/180, 100, 150)
        # print(lines)
        if lines is not None:
            for line in lines:
                for r,theta in line: 
                    # Stores the value of cos(theta) in a 
                    a = np.cos(theta) 
                    # Stores the value of sin(theta) in b 
                    b = np.sin(theta) 
                    # x0 stores the value rcos(theta) 
                    x0 = a*r 
                    # y0 stores the value rsin(theta) 
                    y0 = b*r 
                    # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
                    x1 = int(x0 + 1000*(-b)) 
                    # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
                    y1 = int(y0 + 1000*(a)) 
                    # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
                    x2 = int(x0 - 1000*(-b)) 
                    # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
                    y2 = int(y0 - 1000*(a)) 
                    # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
                    # (0,0,255) denotes the colour of the line to be  
                    #drawn. In this case, it is red.  
                    angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi

                    if abs(angle) <= 10:
                        # print(y1)
                        # print(y2)
                        # cv2.imshow('frame2',frame)
                        # cv2.line(frame,(x1,y1), (x2,y2), (0,0,255),2) 
                        y_pos = max(y1, y2)
    
    cap.release()
    return y_pos, frame            
            # cv2.imshow('frame2',frame)
            # cv2.imshow('white_lines', edges)


            # k = cv2.waitKey(5) & 0xFF
            # if k == 27:
            #     break

    # cap.release()

#     cv2.destroyAllWindows()

# stop_line("http://10.16.135.57:8080/video")