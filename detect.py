# this is a dummy model dont use it for production but you can experiment with it 
#In this code, we capture video from the camera, apply motion detection, and play a buzzer sound when motion is detected. The buzz.wav sound file should be replaced with your own sound file.
#Remember to install the required libraries if you haven't already: "pip install opencv-python-headless pygame"

import cv2
import pygame

# Initialize Pygame for audio
pygame.mixer.init()
buzz_sound = pygame.mixer.Sound("buzz.wav")  # Replace "buzz.wav" with your sound file

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera, change it if needed

# Initialize motion detection parameters
motion_threshold = 10000  # Adjust this threshold as needed
min_contour_area = 500  # Adjust this to filter out small changes
prev_frame = None

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # Convert the frame to grayscale for motion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray
        continue

    frame_delta = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            motion_detected = True
            break

    if motion_detected:
        print("Motion detected")
        buzz_sound.play()  # Play the buzzer sound
    else:
        print("No motion")

    prev_frame = gray

    # Display the video feed (optional)
    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
