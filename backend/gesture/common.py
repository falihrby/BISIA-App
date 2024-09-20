import cv2
import numpy as np

def draw_combined_box(image, landmarks_groups, gesture_label, color=(0, 255, 0), padding=20):
    h, w, _ = image.shape
    valid_points = []

    # Collect valid points from all landmarks groups (both hands)
    for landmarks in landmarks_groups:
        if landmarks is not None and hasattr(landmarks, 'landmark'):
            for landmark in landmarks.landmark:
                valid_points.append(np.array([landmark.x * w, landmark.y * h]))

    if not valid_points:
        return None

    valid_points = np.array(valid_points)

    # Calculate the bounding box coordinates that encompass all points
    min_x = int(np.min(valid_points[:, 0]))
    max_x = int(np.max(valid_points[:, 0]))
    min_y = int(np.min(valid_points[:, 1]))
    max_y = int(np.max(valid_points[:, 1]))

    # Make the bounding box larger to be more visible and encompass both hands
    min_x = max(min_x - padding, 0)
    max_x = min(max_x + padding, w)
    min_y = max(min_y - padding, 0)
    max_y = min(max_y + padding, h)

    # Draw the bounding box around both hands
    cv2.rectangle(image, (min_x, min_y), (max_x, max_y), color, 2)

    # Center the gesture label between both hands, increase text size for visibility
    label_x = min_x + (max_x - min_x) // 2 - 50  # Adjust label position for centering
    label_y = min_y - 20 if min_y - 20 > 0 else min_y + 30  # Place label above or below box

    cv2.putText(image, gesture_label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, color, 3, cv2.LINE_AA)  # Increased font size and thickness

    return min_x, min_y, max_x, max_y

def draw_keypoints_for_debugging(image, *landmarks, circle_size=10):
    h, w, _ = image.shape  # Get the image dimensions

    colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]  # Colors for each hand's keypoints

    # Iterate through provided landmarks (multiple hands can be passed)
    for idx, lm in enumerate(landmarks):
        if lm is not None and hasattr(lm, 'landmark'):
            # Draw all key points for the current hand
            for point in lm.landmark:
                cv2.circle(image, (int(point.x * w), int(point.y * h)), circle_size, colors[idx % len(colors)], -1)
