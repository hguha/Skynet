#Import Libraries
import cv2 as cv


# Assigning our static background to None
static_back = None

# Capture video
cap = cv.VideoCapture(0)

# Iterate through images
while True:
  #Read a frame from the Video
  check, frame = cap.read()

  #Initialize motion to 0 (no motion)
  motion = 0

  #Convert color image to grayscale
  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  
  #Implement gaussian blur on image
  gray = cv.GaussianBlur(gray, (21,21), 0)

  #If this is our first iteration then we assign first
  #frame as static_back
  if static_back is None:
    static_back = gray
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
  cv.imshow("Gray Frame", gray) 
  
  # Displaying the difference in currentframe to 
  # the staticframe(very first_frame) 
  cv.imshow("Difference Frame", diff_frame) 
  
  # Displaying the black and white image in which if 
  # intencity difference greater than 30 it will appear white 
  cv.imshow("Threshold Frame", thresh_frame) 
  
  # Displaying color frame with contour of motion of object 
  cv.imshow("Color Frame", frame) 
  
  key = cv.waitKey(1) 
  # if q entered whole process will stop 
  if key == ord('q'): 
    break

video.release()
cv.destroyAllWindows()  
