import cv2
import numpy as np
import mediapipe as mp

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

draw_color = (0, 0, 255)
brush_thickness = 10
eraser_thickness = 60

canvas = None
xp, yp = 0, 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error")
    exit()

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)

    # Top menu (color / eraser)
    cv2.rectangle(frame, (0, 0), (200, 70), (0, 255, 0), -1)
    cv2.rectangle(frame, (200, 0), (400, 70), (0, 0, 255), -1)
    cv2.rectangle(frame, (400, 0), (640, 70), (50, 50, 50), -1)
    cv2.putText(frame, "ERASER", (450, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            lm = hand_lms.landmark

            x8, y8 = int(lm[8].x * w), int(lm[8].y * h)
            x12, y12 = int(lm[12].x * w), int(lm[12].y * h)

            # Drawing mode (index finger up)
            if y8 < y12:

                # Menu selection
                if y8 < 70:
                    if 0 < x8 < 200:
                        draw_color = (0, 255, 0)
                    elif 200 < x8 < 400:
                        draw_color = (0, 0, 255)
                    elif 400 < x8 < 640:
                        draw_color = (0, 0, 0)

                if xp == 0 and yp == 0:
                    xp, yp = x8, y8

                thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
                cv2.line(canvas, (xp, yp), (x8, y8), draw_color, thickness)

                xp, yp = x8, y8
            else:
                xp, yp = 0, 0

            cv2.circle(frame, (x8, y8), 10, draw_color, -1)
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

    # Merge canvas and frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Virtual Brush", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
