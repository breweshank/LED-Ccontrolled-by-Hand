import cv2
import mediapipe as mp
import serial
import time

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Setup Serial communication with Arduino
arduino = serial.Serial('COM15', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for the connection to establish

# Function to count raised fingers
def count_raised_fingers(hand_landmarks):
    if hand_landmarks:
        fingers = []

        # Thumb
        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if hand_landmarks.landmark[mp_hands.HandLandmark(id * 4)].y < hand_landmarks.landmark[mp_hands.HandLandmark(id * 4 - 2)].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers.count(1)
    return 0

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            num_fingers = count_raised_fingers(hand_landmarks)
            print(f"Raised Fingers: {num_fingers}")

            # Send the number of raised fingers to Arduino
            arduino.write(bytes(str(num_fingers), 'utf-8'))

    else:
        # If no hand is detected, send 0 to Arduino
        arduino.write(bytes('0', 'utf-8'))

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
