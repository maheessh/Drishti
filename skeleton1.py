import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import datetime
import os

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

KNOWN_FACE_WIDTH = 14.0  
FOCAL_LENGTH = 600  
SMOOTHING_WINDOW_SIZE = 10  
face_distance_history = deque(maxlen=SMOOTHING_WINDOW_SIZE)

MOVEMENT_THRESHOLD = 10  
bbox_history = deque(maxlen=5)  

SAVE_FOLDER = "saved_frames"
os.makedirs(SAVE_FOLDER, exist_ok=True)  
def calculate_distance(known_width, width_in_pixels):
    return (known_width * FOCAL_LENGTH) / width_in_pixels

def get_smoothed_distance(new_distance, history):
    history.append(new_distance)
    return np.mean(history)

def is_moving(bbox, history):
    if len(history) == 0:
        return False
    last_bbox = history[-1]
    dx = abs(bbox[0] - last_bbox[0])  
    dy = abs(bbox[1] - last_bbox[1])  
    return (dx > MOVEMENT_THRESHOLD) or (dy > MOVEMENT_THRESHOLD)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

with mp_face_detection.FaceDetection(min_detection_confidence=0.3) as face_detection:
    last_save_time = datetime.datetime.now()  
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_detection.process(rgb_frame)

        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)

                face_width_in_pixels = bbox[2]
                face_distance = calculate_distance(KNOWN_FACE_WIDTH, face_width_in_pixels)
                smoothed_face_distance = get_smoothed_distance(face_distance, face_distance_history)

                if smoothed_face_distance <= 20:
                    if is_moving(bbox, bbox_history):
                        status = "Moving: Someone is approaching you!"
                    else:
                        status = "Still"
                else:
                    status = ""

                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 2)
                cv2.putText(frame, f"Distance: {smoothed_face_distance:.2f} cm", (bbox[0], bbox[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, status, (bbox[0], bbox[1] + bbox[3] + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                bbox_history.append(bbox)

        cv2.imshow("Distance Measurement", frame)

        current_time = datetime.datetime.now()
        if (current_time - last_save_time).total_seconds() >= 5:  # Save every 5 seconds
            filename = os.path.join(SAVE_FOLDER, f"frame_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
            last_save_time = current_time  

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

cap.release()
cv2.destroyAllWindows()
import mediapipe as mp
import numpy as np
from collections import deque
import datetime
import os

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

KNOWN_FACE_WIDTH = 14.0  
FOCAL_LENGTH = 600  
SMOOTHING_WINDOW_SIZE = 10  
face_distance_history = deque(maxlen=SMOOTHING_WINDOW_SIZE)

MOVEMENT_THRESHOLD = 10  
bbox_history = deque(maxlen=5)  
SAVE_FOLDER = "saved_frames"
os.makedirs(SAVE_FOLDER, exist_ok=True)  

def calculate_distance(known_width, width_in_pixels):
    return (known_width * FOCAL_LENGTH) / width_in_pixels

def get_smoothed_distance(new_distance, history):
    history.append(new_distance)
    return np.mean(history)

def is_moving(bbox, history):
    if len(history) == 0:
        return False
    last_bbox = history[-1]
    dx = abs(bbox[0] - last_bbox[0])  
    dy = abs(bbox[1] - last_bbox[1])  
    return (dx > MOVEMENT_THRESHOLD) or (dy > MOVEMENT_THRESHOLD)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

with mp_face_detection.FaceDetection(min_detection_confidence=0.3) as face_detection:
    last_save_time = datetime.datetime.now()  
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_detection.process(rgb_frame)

        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)

                face_width_in_pixels = bbox[2]
                face_distance = calculate_distance(KNOWN_FACE_WIDTH, face_width_in_pixels)
                smoothed_face_distance = get_smoothed_distance(face_distance, face_distance_history)

                if smoothed_face_distance <= 20:
                    if is_moving(bbox, bbox_history):
                        status = "Moving: Someone is approaching you!"
                    else:
                        status = "Still"
                else:
                    status = ""

                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 2)
                cv2.putText(frame, f"Distance: {smoothed_face_distance:.2f} cm", (bbox[0], bbox[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, status, (bbox[0], bbox[1] + bbox[3] + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                bbox_history.append(bbox)

        cv2.imshow("Distance Measurement", frame)

        current_time = datetime.datetime.now()
        if (current_time - last_save_time).total_seconds() >= 5:  
            filename = os.path.join(SAVE_FOLDER, f"frame_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
            last_save_time = current_time  

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

cap.release()
cv2.destroyAllWindows()