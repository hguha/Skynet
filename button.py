import RPi.GPIO as GPIO
import time
import signal
import sys

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def pushButton():
    while True:
        input_state = GPIO.input(23)
        print(input_state)
        if input_state == GPIO.HIGH:
            print('Button Pressed')
            time.sleep(0.2)
        time.sleep(0.2)
        
pushButton()

