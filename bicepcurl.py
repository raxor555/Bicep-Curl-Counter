import cv2
import mediapipe as mp
import numpy as np
import datetime


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 


video_path = "biceps.mp4" 
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}.")
    exit()


counter = 0
stage = None
DOWN_THRESHOLD = 160
UP_THRESHOLD = 30


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break
        
        # Get frame dimensions
        height, width, _ = frame.shape
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Make pose detection
        results = pose.process(image)
        
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks and calculate angle
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates for left arm
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate elbow angle
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize angle
            elbow_pixel = tuple(np.multiply(elbow, [width, height]).astype(int))
            cv2.putText(image, f"{angle:.1f}", 
                       elbow_pixel, 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Curl counter logic
            if angle > DOWN_THRESHOLD:
                stage = "down"
            if angle < UP_THRESHOLD and stage == "down":
                stage = "up"
                counter += 1
                print(f"Curl {counter} at {datetime.datetime.now()}")
                # Log to file
                with open("workout_log.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()}: Curl {counter}\n")
        
        except:
            cv2.putText(image, "No person detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Render curl counter status box
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (15, 12), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                   (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65, 12), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage if stage else "N/A", 
                   (60, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Render pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                 mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        # Display frame
        cv2.imshow('Mediapipe Feed', image)
        
        # Exit on 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()