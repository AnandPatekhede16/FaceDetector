"""
Web-based deployment for Face Recognition System
Creates a simple web interface using Flask
"""

from flask import Flask, render_template, request, jsonify, Response
import cv2
import base64
import io
from PIL import Image
import numpy as np
from data_manager import DataManager
import face_recognition
import threading
import time

app = Flask(__name__)
data_manager = DataManager()

# Global variables for camera
camera = None
camera_lock = threading.Lock()

def init_camera():
    """Initialize camera for web streaming."""
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def get_frame():
    """Get frame from camera for streaming."""
    global camera
    with camera_lock:
        if camera is None:
            init_camera()
        
        ret, frame = camera.read()
        if not ret:
            return None
        
        # Flip frame horizontally
        frame = cv2.flip(frame, 1)
        return frame

def recognize_faces_in_frame(frame):
    """Recognize faces in frame and return annotated frame."""
    try:
        # Load known faces
        known_encodings, known_person_ids = data_manager.get_all_encodings()
        
        if not known_encodings:
            return frame
        
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # Scale back up face locations
        face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            
            if True in matches:
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    person_data = data_manager.get_person_by_id(known_person_ids[best_match_index])
                    if person_data:
                        name = person_data['name']
                        class_name = person_data['class_name']
                        roll_number = person_data['roll_number']
                    else:
                        name = "Unknown"
                        class_name = "Unknown"
                        roll_number = "Unknown"
                else:
                    name = "Unknown Person"
                    class_name = "Unknown"
                    roll_number = "Unknown"
            else:
                name = "Unknown Person"
                class_name = "Unknown"
                roll_number = "Unknown"
            
            # Draw rectangle and text (simplified for web)
            for (top, right, bottom, left) in face_locations:
                color = (0, 255, 0) if name != "Unknown Person" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    except Exception as e:
        print(f"Recognition error: {e}")
        return frame

def generate_frames():
    """Generate frames for video streaming."""
    while True:
        frame = get_frame()
        if frame is None:
            continue
        
        # Add recognition
        frame = recognize_faces_in_frame(frame)
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for registration."""
    try:
        data = request.json
        # This would need to be implemented with proper face capture
        return jsonify({"status": "success", "message": "Registration endpoint - implement face capture"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/persons')
def api_persons():
    """API endpoint to get registered persons."""
    try:
        import pandas as pd
        df = pd.read_csv(data_manager.csv_path)
        persons = df.to_dict('records')
        return jsonify({"status": "success", "persons": persons})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    print("Starting Face Recognition Web Server...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

