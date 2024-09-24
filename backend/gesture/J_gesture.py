import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_j(landmarks1, image, debug=True):
    if landmarks1 is None:
        return False

    # Extract tip and base landmarks for the pinky finger
    pinky_tip = np.array([landmarks1.landmark[20].x, landmarks1.landmark[20].y])
    pinky_base = np.array([landmarks1.landmark[17].x, landmarks1.landmark[17].y])

    # Check if the pinky is oriented horizontally (x difference > y difference)
    is_pinky_horizontal = abs(pinky_tip[0] - pinky_base[0]) > abs(pinky_tip[1] - pinky_base[1])

    # Check if the index, middle, and ring fingers are not fully closed
    is_index_open = landmarks1.landmark[8].y < landmarks1.landmark[6].y  # Index finger tip above middle joint
    is_middle_open = landmarks1.landmark[12].y < landmarks1.landmark[10].y  # Middle finger tip above middle joint
    is_ring_open = landmarks1.landmark[16].y < landmarks1.landmark[14].y  # Ring finger tip above middle joint

    # "J" is detected when the pinky is horizontal and at least one other finger is open
    is_j_shape = is_pinky_horizontal and (is_index_open or is_middle_open or is_ring_open)

    if is_j_shape:
        draw_combined_box(image, [landmarks1], "J", color=(0, 255, 0))

        # Optional debug visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)

        return True

    # Optional debug visualization if "J" shape is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return False
