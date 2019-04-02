import RPi.GPIO as GPIO
import time
import signal
import sys

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

def lightUp(color)
  if color == 'red':
    GPIO.output(9, True)
    time.sleep(1)
    GPIO.output(9, False)
  elif color == 'yellow':
    GPIO.output(10, True)
    time.sleep(1)
    GPIO.output(10, False)
  elif color == 'green':
    GPIO.output(11, True)
    time.sleep(1)
    GPIO.output(11, False)