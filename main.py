import RPi.GPIO as GPIO
import time
import signal
import serial
import sys
import pigpio

RX = 23
pi = pigpio.pi()

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

# Serial
ser = serial.Serial('/dev/ttyAMA0', 115200)

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
  while True:
    #print("#############")
    time.sleep(0.05)    #change the value if needed
    (count, recv) = pi.bb_serial_read(RX)
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
            if distance <= 1200 and strength < 2000:
              print(distance, strength) 
            #else:
              # raise ValueError('distance error: %d' % distance)   
            #i = i + 9

def measureDistance():
    time.sleep(0.1)
    
def activateButton():
    while True:
        input_state = GPIO.input(5)
        if input_state == GPIO.HIGH:
            lightUp('blue')
            lightUp('red')
            lightUp('yellow')
            lightUp('green')
        else:
            lightUp('blue')
            lightDown('red')
            lightDown('yellow')
            lightDown('green')
            measureDistance()
        time.sleep(0.1)
        
        input_state = GPIO.input(4)
        if input_state == GPIO.HIGH:
            cleanUp()
            break
        time.sleep(0.1)
            
def cleanUp():
    # Cleanup GPIO
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    try:
        pi.set_mode(RX, pigpio.INPUT)
        pi.bb_serial_read_open(RX, 115200)
    except:    
        pi.bb_serial_read_close(RX)
        pi.stop()
    print ('Got here!')
    #getTFminiData()
    activateButton()
