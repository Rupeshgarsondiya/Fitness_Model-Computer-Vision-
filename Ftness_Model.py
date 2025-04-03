'''Author : Rupesh Garsondiya
Topic  : Fitness Model (Computer Vision)
github : @Rupeshgarsondiya
Organization : L.J University
'''

# Import necessary libraries

import numpy as np
import cv2  # For real-time computer vision tasks
import mediapipe as mp

# Initialize Mediapipe Pose and Drawing utilities
mp_drawing = mp.solutions.drawing_utils  # Utility for drawing landmarks
mp_pose = mp.solutions.pose  # Pose detection model

# Function to calculate the angle between three points (a, b, c)
def CalAngle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)  # Convert radians to degrees
    return 360 - angle if angle > 180 else angle

# Function to draw repetitions and status on the frame
def draw_info(image, count, status):
    
    cv2.rectangle(image, (0, 0), (225, 73), (255, 255, 255), -1)
    cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(count), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, 'Status', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, status, (80, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv2.LINE_AA)

# Generic function to process exercise
def process_exercise(cap, pose, count_threshold, angle_check_func):
    count, status = 0, None
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            count, status = angle_check_func(landmarks, count, status)
            
            draw_info(image, count, status)

            if count == count_threshold:
                cv2.putText(image, 'Task Completed Successfully', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 165, 255), 3, cv2.LINE_AA)
                cv2.imshow('Completion', image)
                cv2.waitKey(3000)
                break

        except Exception as e:
            print(f'Exception occurred: {e}')

        cv2.imshow('Exercise Tracker', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Dumbbell Forearm Curl function
def angle_check_dumbbell(landmarks, count, status):
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    right_arm_angle = CalAngle(right_shoulder, right_elbow, right_wrist)
    left_arm_angle = CalAngle(left_shoulder, left_elbow, left_wrist)

    if right_arm_angle >= 170 and left_arm_angle >= 170:
        status = 'Down'
    elif right_arm_angle <= 10 and left_arm_angle <= 10 and status == 'Down':
        status = 'Up'
        count += 1
    return count, status

# Function for Dumbbell Forearm Curl
def Dumbbell_Forearm_Curl():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        process_exercise(cap, pose, 10, angle_check_dumbbell)

# Arm Raises function
def angle_check_arm_raises(landmarks, count, status):
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    right_angle = CalAngle(right_hip, right_shoulder, right_wrist)
    left_angle = CalAngle(left_hip, left_shoulder, left_wrist)

    if right_angle <= 20 and left_angle <= 20:
        status = 'Arm down'
    elif (170 <= right_angle <= 180) and (170 <= left_angle <= 180) and status == 'Arm down':
        status = 'Arm up'
        count += 1
    return count, status

# Function for Arm Raises
def Arm_Raises():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        process_exercise(cap, pose, 10, angle_check_arm_raises)

# Side Arm Raise function
def angle_check_side_arm_raise(landmarks, count, status):
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    right_angle = CalAngle(right_wrist, right_shoulder, right_hip)
    left_angle = CalAngle(left_wrist, left_shoulder, left_hip)

    if right_angle <= 20 and left_angle <= 20:
        status = 'Arm down'
    elif right_angle > 80 and left_angle > 80 and status == 'Arm down':
        status = 'Side Arm Raise'
        count += 1
    return count, status

# Function for Side Arm Raise
def Side_Arm_Raise():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        process_exercise(cap, pose, 5, angle_check_side_arm_raise)

# Squats function
def angle_check_squats(landmarks, count, status):
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    right_angle = CalAngle(right_hip, right_knee, right_ankle)
    left_angle = CalAngle(left_hip, left_knee, left_ankle)

    if right_angle >= 170 and left_angle >= 170:
        status = 'Straight body'
    elif right_angle <= 90 and left_angle <= 90 and status == 'Straight body':
        status = 'Bent body'
        count += 1
    return count, status

# Function for Squats
def Squats():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        process_exercise(cap, pose, 3, angle_check_squats)


def angle_check_BackWard_Lunge(landmark,count,status):

    right_hip =  [landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                  landmark[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    
    right_knee = [landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    
    right_ankle = [landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    
    left_hip =  [landmark[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                  landmark[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    
    left_knee = [landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                  landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    
    left_ankle = [landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    
    right_angle = CalAngle(right_hip,right_knee,right_ankle)
    left_angle = CalAngle(left_hip,left_knee,left_ankle)

    

    if right_angle >= 170 or left_angle >= 170:
        status = 'Straight body'
        

    if right_angle <= 95 and left_angle <= 95 and status == 'Straight body':
        count+=1
        status = 'BackWard Lunge'
        
    
    return count ,status

def BackWard_Lunge():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        process_exercise(cap, pose, 3, angle_check_BackWard_Lunge)