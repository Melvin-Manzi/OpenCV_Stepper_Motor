import cv2
import time
import serial
arduino = serial.Serial('COM8', 9600)
time.sleep(2)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
prev_cx, prev_cy = None, None
prev_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    current_time = time.time()
    time_diff = current_time - prev_time if prev_time is not None else 1.0
    direction = ""
    speed = 0.0
    for (x, y, w, h) in faces:
        cx = x + w // 2
        cy = y + h // 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        if prev_cx is not None and prev_cy is not None:
            dx = cx - prev_cx
            dy = cy - prev_cy
            if abs(dx) > 10 or abs(dy) > 10:
                if abs(dx) > abs(dy):
                    direction = "Left" if dx > 0 else "Right"
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            speed = distance / time_diff if time_diff > 0 else 0
            if direction:
                print(f"Direction: {direction}, Speed: {speed:.2f}")
                if direction == "Left":
                    arduino.write(b'L')
                elif direction == "Right":
                    arduino.write(b'R')
        prev_cx, prev_cy = cx, cy
        prev_time = current_time
        break
    cv2.putText(frame, f"Direction: {direction}, Speed: {speed:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('Face Tracker', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
arduino.close()
cv2.destroyAllWindows()
