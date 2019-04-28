import RPi.GPIO as GPIO
import time
import signal
import serial
import sys
import pigpio
import _thread
import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import pygame

ended = False
update= True
static_back=None

def lightUp(color):
    if color == 'blue':
        GPIO.output(17, False)
    elif color == 'red':
        GPIO.output(16, False)
    elif color == 'yellow':
        GPIO.output(13, False)
    elif color == 'green':
        GPIO.output(12, False)
    time.sleep(0.1)
    
def lightDown(color):
    if color == 'blue':
        GPIO.output(17, True)
    elif color == 'red':
        GPIO.output(16, True)
    elif color == 'yellow':
        GPIO.output(13, True)
    elif color == 'green':
        GPIO.output(12, True)
    time.sleep(0.1)
    
def getTFminiData():
    global ended
    RX = 24
    pi = pigpio.pi()
    try:
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 115200)
    except:    
        pi.bb_serial_read_close(RX)
        pi.stop()
    
    while True:
        #print("#############")
        time.sleep(0.05)
        (count, recv) = pi.bb_serial_read(RX)
        #print(count)
        if count > 8:
            for i in range(0, count-9):
                if recv[i] == 89 and recv[i+1] == 89: # 0x59 is 89
                    checksum = 0
                    for j in range(0, 8):
                        checksum = checksum + recv[i+j]
                    checksum = checksum % 256
                    if checksum == recv[i+8]:
                        distance = recv[i+2] + recv[i+3] * 256
                        strength = recv[i+4] + recv[i+5] * 256
                        #print (distance)
                        if distance <= 1200 and strength < 2000:
                            #print(distance, strength)
                            if ended:
                                return
                            if distance <= 50:
                                lightUp('red')
                                lightDown('yellow')
                                pygame.mixer.music.play()
                            elif distance <=100:
                                lightDown('red')
                                lightUp('yellow')
                            else:
                                lightDown('red')
                                lightDown('yellow')
                    break
            
def measureDistance():
    time.sleep(0.1)
    
def activateButton():
    global update
    while True:
        input_state = GPIO.input(5)
        if input_state == GPIO.HIGH:
            lightUp('green')
            update = True
        else:
            lightDown('green')
            measureDistance()
        time.sleep(0.1)
        
        input_state = GPIO.input(4)
        if input_state == GPIO.HIGH:
            cleanUp()
            break
        time.sleep(0.1)

def activateCamera():
    global ended
    global update
    global static_back
    IM_WIDTH = 320
    IM_HEIGHT = 192
    
    # Assigning our static background to None
    static_back = None
      
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    for frames in camera.capture_continuous(rawCapture, format="bgr"):
      frame = frames.array
      rawCapture.truncate(0)
      #Initialize motion to 0 (no motion)
      motion = 0

      #Convert color image to grayscale
      gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
      
      #Implement gaussian blur on image
      gray = cv.GaussianBlur(gray, (21,21), 0)

      #If this is our first iteration then we assign first
      #frame as static_back
      if update == True:
        static_back = gray
        update = False
        print ('updated')
        continue

      # Difference between static background  
      # and current frame(which is GaussianBlur) 
      diff_frame = cv.absdiff(static_back, gray)

      # If change in between static background and 
      # current frame is greater than 30 it will show white color(255) 
      thresh_frame = cv.threshold(diff_frame, 60, 255, cv.THRESH_BINARY)[1] 
      thresh_frame = cv.dilate(thresh_frame, None, iterations = 2)

      # Finding contour of moving object 
      (_, cnts, _) = cv.findContours(thresh_frame.copy(),  
                          cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

      for contour in cnts: 
        if cv.contourArea(contour) < 10000: 
          continue
        motion = 1

        (x, y, w, h) = cv.boundingRect(contour) 
        # making green rectangle arround the moving object 
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 

      # Displaying image in gray_scale 
      #cv.imshow("Gray Frame", gray) 
      
      # Displaying the difference in currentframe to 
      # the staticframe(very first_frame) 
      #cv.imshow("Difference Frame", diff_frame) 
      
      # Displaying the black and white image in which if 
      # intencity difference greater than 30 it will appear white 
      cv.imshow("Threshold Frame", thresh_frame) 
      
      # Displaying color frame with contour of motion of object 
      cv.imshow("Color Frame", frame) 
      
      key = cv.waitKey(1) 
      # if q entered whole process will stop 
      if key == ord('q'): 
        break
      if ended == True:
          return
            
def cleanUp():
    ended=True
    time.sleep(2)
    cv.destroyAllWindows()
    # Cleanup GPIO
    GPIO.cleanup()
    pi.bb_serial_read_close(RX)
    pi.stop()
    sys.exit(0)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("baby.mp3")
    # ignore warning
    GPIO.setwarnings(False)

    # Set Mode
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO
    # blue
    GPIO.setup(17, GPIO.OUT)
    # red
    GPIO.setup(16, GPIO.OUT)
    # yellow
    GPIO.setup(13, GPIO.OUT)
    # green
    GPIO.setup(12, GPIO.OUT)
    # button reset
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # button turn off system
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    lightUp('blue')
    _thread.start_new_thread(getTFminiData, ())
    _thread.start_new_thread(activateButton, ())
    _thread.start_new_thread(activateCamera, ())
