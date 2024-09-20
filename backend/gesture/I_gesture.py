import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Import both functions

def detect_bisindo_i(landmarks1, image, debug=False):
    if landmarks1 is None:
        return False

    # Extract tip and base landmarks for each finger
    thumb_tip = np.array([landmarks1.landmark[4].x, landmarks1.landmark[4].y])
    thumb_base = np.array([landmarks1.landmark[3].x, landmarks1.landmark[3].y])

    index_tip = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    index_base = np.array([landmarks1.landmark[5].x, landmarks1.landmark[5].y])

    middle_tip = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])
    middle_base = np.array([landmarks1.landmark[9].x, landmarks1.landmark[9].y])

    ring_tip = np.array([landmarks1.landmark[16].x, landmarks1.landmark[16].y])
    ring_base = np.array([landmarks1.landmark[13].x, landmarks1.landmark[13].y])

    pinky_tip = np.array([landmarks1.landmark[20].x, landmarks1.landmark[20].y])
    pinky_base = np.array([landmarks1.landmark[17].x, landmarks1.landmark[17].y])

    # Pinky should be open (tip significantly above base)
    is_pinky_open = pinky_tip[1] < pinky_base[1]

    # Other fingers should be closed (tips below bases)
    is_thumb_closed = thumb_tip[1] > thumb_base[1]
    is_index_closed = index_tip[1] > index_base[1]
    is_middle_closed = middle_tip[1] > middle_base[1]
    is_ring_closed = ring_tip[1] > ring_base[1]

    # Count how many fingers are closed (excluding the pinky)
    closed_fingers = sum([is_thumb_closed, is_index_closed, is_middle_closed, is_ring_closed])

    # At least 50% of the fingers (i.e., 2 or more fingers) must be closed
    is_i_shape = is_pinky_open and closed_fingers >= 2

    # Log the detection result
    if is_i_shape:
        draw_combined_box(image, [landmarks1], "I", color=(0, 255, 0))

        # Optional debug visualization
        if debug:
            draw_keypoints_for_debugging(image, landmarks1)

        return True

    # Optional debug visualization if "I" shape is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return False
