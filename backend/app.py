# backend/app.py

from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import threading
from handGestureRecognition import process_frame

app = Flask(__name__)
CORS(app)

# Global variables to control the camera state
camera_active = False
gesture_result = None  # Global variable to store the latest gesture result
camera_lock = threading.Lock()

def generate_frames():
    """Generate frames from the webcam for streaming."""
    global camera_active, gesture_result

    # Initialize the webcam
    with camera_lock:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 15)
        camera_active = True

    if not cap.isOpened():
        raise RuntimeError("Failed to open webcam")

    frame_skip = 2
    frame_count = 0

    while camera_active:
        success, frame = cap.read()
        if not success:
            break

        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        frame_count += 1

        # Resize frame to standard size
        frame = cv2.resize(frame, (640, 480))

        # Process frame for gesture recognition
        gesture_detected, label, processed_frame = process_frame(frame)
        if gesture_detected:
            gesture_result = label  # Store the detected gesture

        # Encode the processed frame as a JPEG image
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()

        # Yield the frame in a streaming format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    """Root endpoint to show basic welcome message."""
    return "Welcome! The video feed is available at /video_feed"

@app.route('/video_feed')
def video_feed():
    """Endpoint to stream the webcam feed."""
    try:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/start_camera')
def start_camera():
    """Endpoint to start the camera."""
    global camera_active
    with camera_lock:
        if camera_active:
            return jsonify({"message": "Camera is already running"}), 200
        camera_active = True
    return jsonify({"message": "Camera started"}), 200

@app.route('/stop_camera')
def stop_camera():
    """Endpoint to stop the camera."""
    global camera_active
    with camera_lock:
        if not camera_active:
            return jsonify({"message": "Camera is already stopped"}), 200
        camera_active = False
    return jsonify({"message": "Camera stopped"}), 200

@app.route('/gesture_result')
def get_gesture_result():
    """Endpoint to fetch the latest gesture result."""
    global gesture_result
    if gesture_result is not None:
        return jsonify({"gesture": gesture_result}), 200
    else:
        return jsonify({"gesture": None}), 200

if __name__ == '__main__':
    app.run(debug=True)
