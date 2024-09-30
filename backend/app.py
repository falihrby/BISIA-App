# backend/app.py
from flask import Flask, Response
from flask_cors import CORS
import cv2
from handGestureRecognition import process_frame

app = Flask(__name__)
CORS(app)

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 15)

    if not cap.isOpened():
        raise RuntimeError("Failed to open webcam")

    frame_skip = 2
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        frame_count += 1

        frame = cv2.resize(frame, (640, 480))
        gesture_detected, label, processed_frame = process_frame(frame)

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return "Welcome! The video feed is available at /video_feed"

@app.route('/video_feed')
def video_feed():
    try:
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
