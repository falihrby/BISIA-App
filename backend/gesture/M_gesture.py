# bisindo_m.py
import numpy as np
from .common import draw_combined_box, draw_keypoints_for_debugging  # Adjust path based on your project structure

def detect_bisindo_m(landmarks1, landmarks2, image, debug=True):
    if landmarks1 is None or landmarks2 is None:
        return False

    # Extract the fingertip landmarks for index, middle, and ring fingers of the first hand
    index_tip_1 = np.array([landmarks1.landmark[8].x, landmarks1.landmark[8].y])
    middle_tip_1 = np.array([landmarks1.landmark[12].x, landmarks1.landmark[12].y])
    ring_tip_1 = np.array([landmarks1.landmark[16].x, landmarks1.landmark[16].y])
    
    # Extract the wrist (0 point) of the second hand
    wrist_2 = np.array([landmarks2.landmark[0].x, landmarks2.landmark[0].y])
    
    # Calculate the distances between the fingertips of the first hand and the wrist of the second hand
    distance_index_wrist = np.linalg.norm(index_tip_1 - wrist_2)
    distance_middle_wrist = np.linalg.norm(middle_tip_1 - wrist_2)
    distance_ring_wrist = np.linalg.norm(ring_tip_1 - wrist_2)

    # Dynamic threshold based on hand size (average of distances from index, middle, and ring to wrist)
    hand_size_1 = np.linalg.norm(index_tip_1 - np.array([landmarks1.landmark[0].x, landmarks1.landmark[0].y]))  # Size of the first hand
    dynamic_threshold = hand_size_1 * 0.8  # Adjust threshold for "M" detection

    # Additional ring finger threshold to prevent confusion with "N"
    ring_threshold = hand_size_1 * 0.7  # Stricter check for ring finger

    # Check if the fingers of the first hand are close to the wrist of the second hand
    is_m_shape = (
        distance_index_wrist < dynamic_threshold and
        distance_middle_wrist < dynamic_threshold and
        distance_ring_wrist < ring_threshold  # Ensure the ring finger is strictly close
    )

    # Ensure the second hand is open (index, middle, ring, pinky extended)
    is_hand2_open = (
        landmarks2.landmark[8].y < landmarks2.landmark[6].y and  # Index finger extended
        landmarks2.landmark[12].y < landmarks2.landmark[10].y and  # Middle finger extended
        landmarks2.landmark[16].y < landmarks2.landmark[14].y and  # Ring finger extended
        landmarks2.landmark[20].y < landmarks2.landmark[18].y  # Pinky finger extended
    )

    # Detect if the gesture matches the "M" shape and the second hand is open
    if is_m_shape and is_hand2_open:
        draw_combined_box(image, [landmarks1, landmarks2], "M", color=(0, 255, 0))

        # Optional: Debug visualization of keypoints
        if debug:
            draw_keypoints_for_debugging(image, landmarks1, landmarks2)
        
        return True

    # Optional: Debug visualization even if "M" is not detected
    if debug:
        draw_keypoints_for_debugging(image, landmarks1, landmarks2)

    return False