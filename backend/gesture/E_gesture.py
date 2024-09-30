import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_e(landmarks1, image, debug=False):
    if landmarks1 is None:
        return False

    # Extract tip landmarks for index, middle, and ring fingers
    index_tip = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    middle_tip = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])
    ring_tip = np.array([landmarks1.landmark[16].x, landmarks1.landmark[16].y])

    # Calculate distances between the finger tips for the E shape detection
    distance_index_middle = np.linalg.norm(index_tip - middle_tip)
    distance_middle_ring = np.linalg.norm(middle_tip - ring_tip)

    # Define dynamic threshold based on hand size for proximity between finger tips
    hand_size = np.linalg.norm(index_tip - np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]))
    dynamic_threshold_e = hand_size * 0.4  # Adjusted threshold for finer detection

    # Check if other fingers are closed (thumb and pinky)
    thumb_tip = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])
    thumb_base = np.array([landmarks1.landmark[3].x, landmarks1.landmark[3].y])
    pinky_tip = np.array([landmarks1.landmark[20].x, landmarks1.landmark[20].y])
    pinky_base = np.array([landmarks1.landmark[18].x, landmarks1.landmark[18].y])

    is_thumb_closed = thumb_tip[1] > thumb_base[1]  # Thumb should be closed (downward)
    is_pinky_closed = pinky_tip[1] > pinky_base[1]  # Can be relaxed if required

    # Check if the index, middle, and ring fingers are close together
    is_fingers_close = (
        distance_index_middle < dynamic_threshold_e and
        distance_middle_ring < dynamic_threshold_e
    )

    # Adjust detection logic to allow some flexibility on pinky closure
    is_e_shape = is_fingers_close and is_thumb_closed

    # If the E shape is detected, draw the bounding box
    if is_e_shape:
        draw_combined_box(image, [landmarks1], "E", color=(0, 255, 0))

        # Optional debug visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)

        return True

    # Optional debug visualization if "E" shape is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return False
