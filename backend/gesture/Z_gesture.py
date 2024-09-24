import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging

def detect_bisindo_z(landmarks1, image, debug=True):
    if landmarks1 is None:
        return False

    # Get image dimensions
    h, w, _ = image.shape

    # Extract the coordinates for the finger tips and knuckles
    finger_tips = [
        np.array([landmarks1.landmark[8].x * w, landmarks1.landmark[8].y * h]),   # Index tip
        np.array([landmarks1.landmark[12].x * w, landmarks1.landmark[12].y * h]),  # Middle tip
        np.array([landmarks1.landmark[16].x * w, landmarks1.landmark[16].y * h]),  # Ring tip
        np.array([landmarks1.landmark[20].x * w, landmarks1.landmark[20].y * h])   # Pinky tip
    ]
    finger_knuckles = [
        np.array([landmarks1.landmark[6].x * w, landmarks1.landmark[6].y * h]),   # Index knuckle
        np.array([landmarks1.landmark[10].x * w, landmarks1.landmark[10].y * h]), # Middle knuckle
        np.array([landmarks1.landmark[14].x * w, landmarks1.landmark[14].y * h]), # Ring knuckle
        np.array([landmarks1.landmark[18].x * w, landmarks1.landmark[18].y * h])  # Pinky knuckle
    ]

    # Check if all fingers are folded (i.e., the tips are below the knuckles)
    def fingers_are_closed(tips, knuckles):
        return all(tip[1] > knuckle[1] for tip, knuckle in zip(tips, knuckles))

    # Extract wrist and palm base points
    wrist = np.array([landmarks1.landmark[0].x * w, landmarks1.landmark[0].y * h])  # Wrist
    palm_base_1 = np.array([landmarks1.landmark[1].x * w, landmarks1.landmark[1].y * h])  # Base near thumb
    palm_base_5 = np.array([landmarks1.landmark[5].x * w, landmarks1.landmark[5].y * h])  # Base near pinky

    # Check if the wrist is bent by comparing the Y-coordinate of the wrist with the palm base
    def wrist_is_bent(wrist, palm_base_1, palm_base_5, threshold=0.05):
        palm_center = (palm_base_1 + palm_base_5) / 2  # Calculate palm center
        wrist_distance = np.linalg.norm(wrist - palm_center)
        avg_hand_size = np.linalg.norm(palm_base_1 - palm_base_5)  # Hand size
        proximity_threshold = avg_hand_size * threshold
        return wrist_distance > proximity_threshold  # Wrist is bent if it's displaced from palm center

    are_fingers_closed = fingers_are_closed(finger_tips, finger_knuckles)
    is_wrist_bent = wrist_is_bent(wrist, palm_base_1, palm_base_5)

    # Detect the "Z" gesture
    is_bisindo_z = are_fingers_closed and is_wrist_bent

    if is_bisindo_z:
        draw_combined_box(image, [landmarks1], "Z", color=(0, 255, 0))

    # Optional debug visualization
    if debug:
        draw_keypoints_for_debugging(image, landmarks1)

    return is_bisindo_z
