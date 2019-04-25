import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 115200)

def getTFminiData():
    while True:
      count = ser.inWaiting()
      print('count', count)
      if count > 8:
        print('in while-loop')
        recv = ser.read(9)
        ser.reset_input_buffer()
        print('recv[0]', recv[0])
        if recv[0] ==0x59 and rec[1] == 0x59:
          
          distance = recv[2] + recv[3] * 256
          strength = recv[4] + recv[5] * 256
          print('(', distance, ', ', strength, ')')
          ser.reset_input_buffer()

if __name__ == '__main__':
  try:
    if ser.is_open == False:
      print('not open')
      ser.open()
    print('is open')
    getTFminiData()
  except KeyboardInterrupt:
    if ser != None:
      ser.close()
