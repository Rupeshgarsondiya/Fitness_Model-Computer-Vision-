import cv2
import time
import streamlit as st
import Ftness_Model as fm  # Import fitness model functions

from Ftness_Model import CalAngle, draw_info, Arm_Raises, Squats, Side_Arm_Raise,BackWard_Lunge, Dumbbell_Forearm_Curl


'''
# Streamlit UI
st.title("Personalized AI Trainer: Computer Vision")

st.header("Project Description")
st.write("This project is Fitness and pose estimation based on computer vision.")
st.write("Live video feed is processed using OpenCV, and pose estimation is done via MediaPipe.")
st.write("The system supports multiple exercises with real-time analysis.")

# Initialize session state for camera handling
if "camera" not in st.session_state:
    st.session_state.camera = None
if "prev_exercise" not in st.session_state:
    st.session_state.prev_exercise = None

# Exercise selection
exercise_type = st.radio(
    "Select the exercise type:",
    options=["Dumbbell Forearm Curl", "Arm Raise", "Side Arm Raise", "Squats", "Backward Lunge"],
    index=None  # No selection initially
)

# Function to release the camera safely
def release_camera():
    if st.session_state.camera is not None:
        st.session_state.camera.release()
        st.session_state.camera = None

# Function to map exercises to their corresponding function
def get_exercise_function(exercise_name):
    exercise_map = {
        "Dumbbell Forearm Curl": Dumbbell_Forearm_Curl,  # Instantiate class
        "Arm Raise": Arm_Raises,
        "Side Arm Raise": Side_Arm_Raise,
        "Squats": Squats,
        "Backward Lunge": BackWard_Lunge
    }
    return exercise_map.get(exercise_name, None)() if exercise_name in exercise_map else None
    
# If an exercise is selected
if exercise_type:
    # Check if the exercise type has changed
    if exercise_type != st.session_state.prev_exercise:
        release_camera()  # Release previous camera feed
        st.session_state.prev_exercise = exercise_type  # Update selected exercise
        time.sleep(1)  # Small delay to ensure the camera resets

    # Open the camera feed
    st.session_state.camera = cv2.VideoCapture(0)
    if not st.session_state.camera.isOpened():
        st.error("Error: Unable to access the camera.")
    else:
        frame_placeholder = st.empty()  # Placeholder for live frames

        # Get the function corresponding to the selected exercise
        exercise_function = get_exercise_function(exercise_type)

        if exercise_function:
            while True:
                ret, frame = st.session_state.camera.read()
                if not ret:
                    st.error("Failed to grab frame.")
                    break

                # Convert frame for Streamlit display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                try:
                    # Call the specific exercise method
                    processed_frame = exercise_function.process(frame)
                except AttributeError:
                    st.error(f"Error: {exercise_type} does not have a 'process' method.")
                    break

                # Display processed frame
                frame_placeholder.image(processed_frame, channels="RGB")

                # Stop the loop if user switches the exercise
                if exercise_type != st.session_state.prev_exercise:
                    break

# Display selected exercise
if exercise_type:
    st.write(f"You selected: {exercise_type}")

'''

Dumbbell_Forearm_Curl()
Arm_Raises()
Side_Arm_Raise,BackWard_Lunge()
Squats()
BackWard_Lunge()
