import cv2
import numpy as np
import time

# cap = cv2.VideoCapture("http://192.168.0.42:8091/?action=stream")
cap = cv2.VideoCapture("http://10.16.135.57:8080/video")

while(cap.isOpened()):

    frameId = int(round(cap.get(1)))
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    ret, frame = cap.read()

    if(ret):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #white
        mask0 = cv2.inRange(hsv, (0,0,180), (180,38,255))

        ## Merge the mask and crop the red regions
        imgThreshHigh_white = cv2.bitwise_and(frame, frame, mask=mask0)

        thresh_white = cv2.medianBlur(imgThreshHigh_white,5)
        thresh_white = cv2.threshold(thresh_white, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

        thresh_white = cv2.erode(thresh_white, None, iterations=2)
        thresh_white = cv2.dilate(thresh_white, None, iterations=4)
        # lines = cv2.HoughLinesP(thresh_white, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)

        # print(lines)

        # red
        mask1 = cv2.inRange(hsv, (0,50,20), (5,255,255))
        mask2 = cv2.inRange(hsv, (175,50,20), (180,255,255))

        ## Merge the mask and crop the red regions
        mask = cv2.bitwise_or(mask1, mask2)
        imgThreshHigh_red = cv2.bitwise_and(frame, frame, mask=mask)

        thresh_red = cv2.medianBlur(imgThreshHigh_red,5)
        thresh_red = cv2.threshold(imgThreshHigh_red, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

        thresh_red = cv2.erode(thresh_red, None, iterations=2)
        thresh_red = cv2.dilate(thresh_red, None, iterations=4)

        # yellow
        mask3 = cv2.inRange(hsv, (21,39,64), (40,255,255))

        ## Merge the mask and crop the red regions
        imgThreshHigh_yellow = cv2.bitwise_and(frame, frame, mask=mask3)

        thresh_yellow = cv2.medianBlur(imgThreshHigh_yellow,5)
        thresh_yellow = cv2.threshold(thresh_yellow, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

        thresh_yellow = cv2.erode(thresh_yellow, None, iterations=2)
        thresh_yellow = cv2.dilate(thresh_yellow, None, iterations=4)

        #green
        mask4 = cv2.inRange(hsv, (41,39,64), (80,255,255))

        ## Merge the mask and crop the red regions
        imgThreshHigh_green = cv2.bitwise_and(frame, frame, mask=mask4)

        thresh_green = cv2.medianBlur(imgThreshHigh_green,5)
        thresh_green = cv2.threshold(thresh_green, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

        thresh_green = cv2.erode(thresh_green, None, iterations=2)
        thresh_green = cv2.dilate(thresh_green, None, iterations=4)       
    
        circles = cv2.HoughCircles(cv2.cvtColor(thresh_green, cv2.COLOR_BGR2GRAY),cv2.HOUGH_GRADIENT,1,500,
                            param1=200,param2=10,minRadius=5,maxRadius=100)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
        
           
        # print(circles)
        cv2.imshow('frame',frame)
        # cv2.imshow('edges',edges)
        cv2.imshow('white_lines', thresh_white)
        cv2.imshow('red_circles', thresh_red)
        cv2.imshow('yellow_circles', thresh_yellow)
        cv2.imshow('green_circles', thresh_green)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

cap.release()

cv2.destroyAllWindows()
