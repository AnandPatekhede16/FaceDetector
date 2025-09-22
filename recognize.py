"""
Face Recognition Module
Real-time face detection and recognition using webcam.
"""

import cv2
import face_recognition
import numpy as np
from data_manager import DataManager
import time


class FaceRecognizer:
    """Face recognition system for real-time detection and identification."""
    
    def __init__(self, tolerance=0.6):
        """
        Initialize the face recognizer.
        
        Args:
            tolerance (float): Face recognition tolerance (lower = more strict)
        """
        self.tolerance = tolerance
        self.data_manager = DataManager()
        self.known_encodings = []
        self.known_person_ids = []
        self.known_names = []
        self.known_classes = []
        self.known_roll_numbers = []
        
        # Load existing data
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load all known face encodings and person details."""
        try:
            # Get all encodings and person IDs
            self.known_encodings, self.known_person_ids = self.data_manager.get_all_encodings()
            
            if not self.known_encodings:
                print("No registered faces found. Please register some faces first.")
                return
            
            # Load person details for each ID
            for person_id in self.known_person_ids:
                person_data = self.data_manager.get_person_by_id(person_id)
                if person_data:
                    self.known_names.append(person_data['name'])
                    self.known_classes.append(person_data['class_name'])
                    self.known_roll_numbers.append(person_data['roll_number'])
            
            print(f"Loaded {len(self.known_encodings)} registered faces.")
            
        except Exception as e:
            print(f"Error loading known faces: {str(e)}")
            self.known_encodings = []
            self.known_person_ids = []
    
    def recognize_faces_in_frame(self, frame):
        """
        Recognize faces in a given frame.
        
        Args:
            frame: OpenCV frame/image
            
        Returns:
            list: List of (name, class_name, roll_number, confidence) for each face
        """
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_info = []
        
        for face_encoding in face_encodings:
            if not self.known_encodings:
                face_info.append(("Unknown Person", "Unknown", "Unknown", 0.0))
                continue
            
            # Compare with known faces
            matches = face_recognition.compare_faces(
                self.known_encodings, face_encoding, tolerance=self.tolerance
            )
            
            if True in matches:
                # Find the best match
                face_distances = face_recognition.face_distance(
                    self.known_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    confidence = 1 - face_distances[best_match_index]
                    name = self.known_names[best_match_index]
                    class_name = self.known_classes[best_match_index]
                    roll_number = self.known_roll_numbers[best_match_index]
                    face_info.append((name, class_name, roll_number, confidence))
                else:
                    face_info.append(("Unknown Person", "Unknown", "Unknown", 0.0))
            else:
                face_info.append(("Unknown Person", "Unknown", "Unknown", 0.0))
        
        return face_locations, face_info
    
    def draw_face_info(self, frame, face_locations, face_info):
        """
        Draw face information on the frame.
        
        Args:
            frame: OpenCV frame
            face_locations: List of face locations
            face_info: List of face information tuples
            
        Returns:
            frame: Frame with drawn information
        """
        # Scale back up face locations since the frame was scaled to 1/4 size
        face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]
        
        for (top, right, bottom, left), (name, class_name, roll_number, confidence) in zip(face_locations, face_info):
            # Draw rectangle around face
            color = (0, 255, 0) if name != "Unknown Person" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Prepare text
            if name != "Unknown Person":
                text = f"{name} ({class_name})"
                confidence_text = f"Confidence: {confidence:.2f}"
                roll_text = f"Roll: {roll_number}"
            else:
                text = "Unknown Person"
                confidence_text = ""
                roll_text = ""
            
            # Draw text background
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, (left, bottom - 60), (left + text_size[0] + 10, bottom), color, -1)
            
            # Draw text
            cv2.putText(frame, text, (left + 5, bottom - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            if confidence_text:
                cv2.putText(frame, confidence_text, (left + 5, bottom - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            if roll_text:
                cv2.putText(frame, roll_text, (left + 5, bottom - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def run_recognition(self):
        """Run the real-time face recognition system."""
        # Check if we have any registered faces
        if not self.known_encodings:
            print("No registered faces found. Please run register.py first to add some faces.")
            return
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("Face Recognition System Started!")
        print("Press 'q' to quit, 'r' to reload faces, 't' to toggle tolerance")
        print(f"Current tolerance: {self.tolerance}")
        print(f"Registered faces: {len(self.known_encodings)}")
        
        # Set webcam properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        frame_count = 0
        fps_start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read from webcam")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process every other frame for better performance
                if frame_count % 2 == 0:
                    face_locations, face_info = self.recognize_faces_in_frame(frame)
                    frame = self.draw_face_info(frame, face_locations, face_info)
                
                # Calculate and display FPS
                frame_count += 1
                if frame_count % 30 == 0:
                    fps_end_time = time.time()
                    fps = 30 / (fps_end_time - fps_start_time)
                    fps_start_time = fps_end_time
                    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display frame
                cv2.imshow('Face Recognition System', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    print("Reloading faces...")
                    self.load_known_faces()
                elif key == ord('t'):
                    self.tolerance = 0.9 if self.tolerance == 0.6 else 0.6
                    print(f"Tolerance changed to: {self.tolerance}")
        
        except KeyboardInterrupt:
            print("\nRecognition stopped by user")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Face recognition system stopped.")


def main():
    """Main function to run face recognition."""
    print("Welcome to Face Recognition System!")
    
    # Initialize recognizer
    recognizer = FaceRecognizer(tolerance=0.6)
    
    # Check if we have registered faces
    if not recognizer.known_encodings:
        print("\nNo registered faces found.")
        print("Please run 'python register.py' first to register some faces.")
        return
    
    print(f"\nStarting recognition with {len(recognizer.known_encodings)} registered faces...")
    
    # Run recognition
    recognizer.run_recognition()


if __name__ == "__main__":
    main()

