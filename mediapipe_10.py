import cv2
import mediapipe as mp
import math
import time
from socketIO_client import SocketIO

# IP Server (String number)
CONNECT_TO_SERVER = True # True / False
SERVER_IP = '34.125.103.10' # localhost | i.p.ser.ver

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

encendido = False
msg = ""
toque1 = False
toque2 = False

socketIO = SocketIO(SERVER_IP, 5001)

# For webcam input:

cap = cv2.VideoCapture(1)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    cv2.rectangle(image, (100,100), (100,200), (0,255,0), 20)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
            y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)
            x2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width)
            y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height)
            cv2.circle(image, (x1,y1),3,(255,0,0),3)
            cv2.circle(image, (x2,y2),3,(255,0,0),3)
            cv2.circle(image, (100,310),3,(0,0,255),3)
            distanceFF = int(math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1))))
            time.sleep(0.005)
            print(str(y1) + " OFF")
            if distanceFF <= 27 and 75 < x1 <145 and 315 > y1 > 180 and CONNECT_TO_SERVER:
                socketIO.emit("nuevo_mensaje",str(y1))
                cv2.circle(image, (100,y1), 20, (0,255,0), -1)
                cv2.rectangle(image, (100,100), (100,y1), (0,255,0), 20)
                if 175 < y1 < 220:
                    toque1= True
                if y1 > 300:
                    toque2 = True
                    if toque1 == True and toque2 == True:
                        if encendido == True: encendido = False; socketIO.emit("nuevo_mensaje","OFF"); toque1 = False; continue
                        elif encendido == False: encendido = True; socketIO.emit("nuevo_mensaje","ON"); toque1 = False; continue
                    time.sleep(0.05)
            else: socketIO.emit("nuevo_mensaje","SOLTADO"); toque1= False; toque2 = False

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()