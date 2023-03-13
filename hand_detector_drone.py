import cv2
import mediapipe as mp
from djitellopy import Tello

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#####
tello_cam = 0 # poner a 1 si se tiene la camara del tello
#####

if tello_cam: 
  drone = Tello()
  drone.connect()
  drone.for_back_velocity = 0
  drone.left_right_velocity = 0
  drone.up_down_velocity = 0
  drone.yaw_velocity = 0
  drone.speed = 0
  print("Batería: ", drone.get_battery(), "%")
  drone.streamoff()
  drone.streamon()
else:
  # For webcam input:
  cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while True:
    if tello_cam == 1:
      frame_read = drone.get_frame_read()
      image = frame_read.frame
    else:
      success, image = cap.read()


    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()