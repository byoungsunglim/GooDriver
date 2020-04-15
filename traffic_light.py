import cv2
from threading import Thread
import queue
import numpy as np
import time
from stop_check import stop_check
from stop_line import stop_line
import serial
import os

def multistream(stream):
    ret, frame = stream.read()
    return frame

def traffic_light(ip_cam):
    ser = serial.Serial('/dev/rfcomm1')  # open serial port

    colors = ['RED', 'YELLOW', 'GREEN']
    lights = [0, 0, 0]
    frame_count = 0

    line_limit = 150
    y_pos = 0
    last_color = 'NONE'
    is_goodriver = True

    cap = cv2.VideoCapture(ip_cam)
    # cap2 = cv2.VideoCapture(ip_cam2)

    # cam1 = Thread(target=multistream, args=(cap, ))
    # cam2 = Thread(target=multistream, args=(cap2, ))

    # cam1.start()
    # cam2.start()
    # cam1.join()
    # cam2.join()

    while(cap.isOpened()):
        ret, frame = cap.read()
        # ret2, frame2 = cap2.read()

        if(ret):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
           
            # red light
            mask1 = cv2.inRange(hsv, (0,50,20), (5,255,255))
            mask2 = cv2.inRange(hsv, (175,50,20), (180,255,255))

            ## Merge the mask and crop the red regions
            mask = cv2.bitwise_or(mask1, mask2)
            imgThreshHigh_red = cv2.bitwise_and(frame, frame, mask=mask)

            thresh_red = cv2.medianBlur(imgThreshHigh_red,5)
            thresh_red = cv2.threshold(imgThreshHigh_red, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

            thresh_red = cv2.erode(thresh_red, None, iterations=2)
            thresh_red = cv2.dilate(thresh_red, None, iterations=4)

            circles_red = cv2.HoughCircles(cv2.cvtColor(thresh_red, cv2.COLOR_BGR2GRAY),cv2.HOUGH_GRADIENT,1,500,
                                param1=450,param2=10,minRadius=30,maxRadius=100)

            if circles_red is not None:
                circles_red = np.uint16(np.around(circles_red))
                for i in circles_red[0,:]:
                    # draw the outer circle
                    cv2.circle(frame,(i[0],i[1]),i[2],(255,0,0),2)
                    # draw the center of the circle
                    cv2.circle(frame,(i[0],i[1]),2,(0,0,0),3)

                    lights[0] += i[2]

            # yellow light
            mask3 = cv2.inRange(hsv, (21,39,64), (40,255,255))

            imgThreshHigh_yellow = cv2.bitwise_and(frame, frame, mask=mask3)

            thresh_yellow = cv2.medianBlur(imgThreshHigh_yellow,5)
            thresh_yellow = cv2.threshold(thresh_yellow, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

            thresh_yellow = cv2.erode(thresh_yellow, None, iterations=2)
            thresh_yellow = cv2.dilate(thresh_yellow, None, iterations=4)

            circles_yellow = cv2.HoughCircles(cv2.cvtColor(thresh_yellow, cv2.COLOR_BGR2GRAY),cv2.HOUGH_GRADIENT,1,500,
                                param1=500,param2=15,minRadius=30,maxRadius=100)

            if circles_yellow is not None:
                circles_yellow = np.uint16(np.around(circles_yellow))
                for i in circles_yellow[0,:]:
                    # draw the outer circle
                    cv2.circle(frame,(i[0],i[1]),i[2],(255,255,0),2)
                    # draw the center of the circle
                    cv2.circle(frame,(i[0],i[1]),2,(0,0,0),3)

                    lights[1] += i[2]

            #green light
            mask4 = cv2.inRange(hsv, (41,39,64), (80,255,255))

            imgThreshHigh_green = cv2.bitwise_and(frame, frame, mask=mask4)

            thresh_green = cv2.medianBlur(imgThreshHigh_green,5)
            thresh_green = cv2.threshold(thresh_green, 100, 255, cv2.THRESH_BINARY)[1] #This operation takes any pixel value p >= 200 and sets it to 255 (white). Pixel values < 200 are set to 0 (black).

            thresh_green = cv2.erode(thresh_green, None, iterations=2)
            thresh_green = cv2.dilate(thresh_green, None, iterations=4)       
        
            circles_green = cv2.HoughCircles(cv2.cvtColor(thresh_green, cv2.COLOR_BGR2GRAY),cv2.HOUGH_GRADIENT,1,500,
                                param1=500,param2=15,minRadius=30,maxRadius=100)

            if circles_green is not None:
                circles_green = np.uint16(np.around(circles_green))
                for i in circles_green[0,:]:
                    # draw the outer circle
                    cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(frame,(i[0],i[1]),2,(0,0,0),3)

                    lights[2] += i[2]

            cv2.imshow('frame',frame)
            

            frame_count += 1

            
            if frame_count % 5 == 0:
                if sum(lights) == 0:
                    print('NONE')
                else:
                    current_color = colors[lights.index(max(lights))]
                    ser.write(str.encode(current_color))
                    print("TRAFFIC COLOR ---> " + current_color)
                    
                    # print("y pos: " + str(y_pos))
                    # print("is_goodriver: " + str(is_goodriver))
                    if current_color == 'RED' and is_goodriver == True:
                        y_pos, edges = stop_line("http://10.16.135.57:8080/video")
                        cv2.imshow('edges',edges)
                        if y_pos > line_limit:
                            is_goodriver = False
                            os.system('spd-say "Bad Driver"')
                            # print("is goodriver  fff:" + str(is_goodriver))
                            ser.write(str.encode("Bad Driver"))
                            print("Bad Driver >_________<")


                    if last_color == 'RED' and current_color == 'GREEN' and is_goodriver == True:
                        y_pos, edges = stop_line("http://10.16.135.57:8080/video")
                        cv2.imshow('edges',edges)
                        if y_pos <= line_limit:
                            os.system('spd-say "Good Driver"')
                            ser.write(str.encode("Good Driver"))
                            print("Good Driver ^_________^")

                    if current_color != 'RED':
                        y_pos = 0
                        is_goodriver = True

                    last_color = current_color
                    # print("last color: " + last_color)
                    # print("is goodriver ## " + str(is_goodriver))
                    lights = [0, 0, 0]

                    
            
            # cv2.imshow('red_circles', thresh_red)
            # cv2.imshow('yellow_circles', thresh_yellow)
            # cv2.imshow('green_circles', thresh_green)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

    cap.release()

    cv2.destroyAllWindows()

traffic_light("http://10.16.129.156:8080/video")