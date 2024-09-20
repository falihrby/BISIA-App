import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_l(landmarks1, image, debug=False):
    # Only proceed if there is at least one hand detected (landmarks1)
    if landmarks1 is None:
        return False

    # Extract landmarks for index finger (points 8, 7, 5) and thumb (points 4, 3, 2)
    index_tip = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    index_base = np.array([landmarks1.landmark[5].x, landmarks1.landmark[5].y])

    thumb_tip = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])
    thumb_base = np.array([landmarks1.landmark[2].x, landmarks1.landmark[2].y])

    # Check if the index finger is upright (tip higher than base)
    is_index_upright = index_tip[1] < index_base[1]  # y-axis is inverted, lower y means higher

    # Check if the thumb is horizontal (thumb tip and base are horizontally aligned)
    is_thumb_horizontal = abs(thumb_tip[1] - thumb_base[1]) < 0.15  # Smaller threshold for better detection

    # Add angle check between thumb and index to differentiate from "C"
    index_vector = index_tip - index_base
    thumb_vector = thumb_tip - thumb_base
    angle_between = np.degrees(np.arccos(np.dot(index_vector, thumb_vector) / 
                            (np.linalg.norm(index_vector) * np.linalg.norm(thumb_vector))))

    # Ensure that the thumb and index finger are forming an "L" (angle close to 90 degrees)
    is_l_shape = 80 <= angle_between <= 100

    # Check if the other fingers (middle, ring, and pinky) are closed
    are_other_fingers_folded = (
        landmarks1.landmark[12].y > landmarks1.landmark[10].y and  # Middle finger folded
        landmarks1.landmark[16].y > landmarks1.landmark[14].y and  # Ring finger folded
        landmarks1.landmark[20].y > landmarks1.landmark[18].y      # Pinky finger folded
    )

    # Detect the gesture only if all conditions for "L" are met
    if is_index_upright and is_thumb_horizontal and is_l_shape and are_other_fingers_folded:
        draw_combined_box(image, [landmarks1], "L", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)
        
        return True
    else:
        # Optional: Debug visualization if "L" is not detected
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)

    return False
