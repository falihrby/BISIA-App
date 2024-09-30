import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging

def detect_bisindo_u(landmarks1, image, debug=False):
    if landmarks1 is None:
        return False

    # Get hand size for scaling thresholds
    h, w, _ = image.shape
    thumb_tip = np.array([landmarks1.landmark[4].x * w, landmarks1.landmark[4].y * h])  # Thumb tip
    index_tip = np.array([landmarks1.landmark[8].x * w, landmarks1.landmark[8].y * h])  # Index tip

    # Calculate the distances between thumb and index finger
    x_distance = np.abs(thumb_tip[0] - index_tip[0])  # Horizontal distance
    y_distance = np.abs(thumb_tip[1] - index_tip[1])  # Vertical distance

    # Calculate hand size based on the distance between index tip and wrist
    wrist = np.array([landmarks1.landmark[0].x * w, landmarks1.landmark[0].y * h])  # Wrist position
    hand_size = np.linalg.norm(index_tip - wrist)

    # Define thresholds based on hand size
    x_threshold = hand_size * 0.4  # Parallel distance (horizontal closeness)
    y_threshold = hand_size * 0.5  # Vertical distance to ensure both fingers are "up"

    # Check if thumb and index finger are nearly parallel and close together
    are_parallel_and_close = x_distance < x_threshold and y_distance < y_threshold

    # Check if both points 4 (thumb) and 8 (index) are facing upwards (above wrist)
    are_fingers_up = (thumb_tip[1] < wrist[1]) and (index_tip[1] < wrist[1])

    # Ensure other fingers (middle, ring, pinky) are folded
    def are_other_fingers_folded(landmarks):
        folded = True
        for i in [12, 16, 20]:  # Middle, Ring, Pinky tips
            if landmarks.landmark[i].y < landmarks.landmark[i - 2].y:  # Ensure folded (tip below corresponding middle joint)
                folded = False
        return folded

    other_fingers_folded = are_other_fingers_folded(landmarks1)

    # Check if the conditions for the letter "U" are satisfied
    is_bisindo_u = are_parallel_and_close and are_fingers_up and other_fingers_folded

    # Draw bounding box if the gesture is detected
    if is_bisindo_u:
        draw_combined_box(image, [landmarks1], "U", color=(0, 255, 0))

    # Optional debug visualization
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return is_bisindo_u
