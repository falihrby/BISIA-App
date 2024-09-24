import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_o(landmarks, image, debug=True):
    if landmarks is None:
        return False

    # Extract the thumb (4) and index finger (8) tip points
    thumb_tip = np.array([landmarks.landmark[4].x, landmarks.landmark[4].y])
    index_tip = np.array([landmarks.landmark[8].x, landmarks.landmark[8].y])

    # Calculate the distance between thumb and index finger tips
    distance_thumb_index = np.linalg.norm(thumb_tip - index_tip)

    # Define a small threshold to detect if thumb and index finger tips are touching
    touch_threshold = 0.08  # Adjust this value depending on the scale of your image

    # Check if thumb and index finger tips are close enough to be considered touching
    is_thumb_index_touching = distance_thumb_index < touch_threshold

    # Ensure the other fingers (middle, ring, pinky) are open (extended)
    is_middle_open = landmarks.landmark[12].y < landmarks.landmark[10].y  # Middle finger
    is_ring_open = landmarks.landmark[16].y < landmarks.landmark[14].y  # Ring finger
    is_pinky_open = landmarks.landmark[20].y < landmarks.landmark[18].y  # Pinky finger

    # Check if all conditions for the letter "O" are met
    is_o_shape = is_thumb_index_touching and is_middle_open and is_ring_open and is_pinky_open

    # Detect if the gesture matches the "O" shape
    if is_o_shape:
        draw_combined_box(image, [landmarks], "O", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks)
        
        return True

    # Optional: Debug visualization even if "O" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks)

    return False
