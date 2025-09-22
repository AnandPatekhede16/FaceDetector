"""
Data management utilities for face recognition system.
Handles CSV storage for person details and pickle storage for face encodings.
"""

import pandas as pd
import pickle
import os
from typing import List, Dict, Any, Optional
import face_recognition
import cv2
import numpy as np


class DataManager:
    """Manages data storage and retrieval for the face recognition system."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize DataManager with data directory.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self.csv_path = os.path.join(data_dir, "person_details.csv")
        self.encodings_path = os.path.join(data_dir, "face_encodings.pkl")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize CSV file if it doesn't exist
        self._init_csv()
        
        # Load existing encodings
        self.encodings = self._load_encodings()
    
    def _init_csv(self):
        """Initialize CSV file with required columns if it doesn't exist."""
        if not os.path.exists(self.csv_path):
            df = pd.DataFrame(columns=[
                'id', 'name', 'class_name', 'roll_number', 'email', 'phone', 'registration_date'
            ])
            df.to_csv(self.csv_path, index=False)
    
    def _load_encodings(self) -> Dict[int, List[float]]:
        """Load face encodings from pickle file."""
        if os.path.exists(self.encodings_path):
            with open(self.encodings_path, 'rb') as f:
                return pickle.load(f)
        return {}
    
    def _save_encodings(self):
        """Save face encodings to pickle file."""
        with open(self.encodings_path, 'wb') as f:
            pickle.dump(self.encodings, f)
    
    def get_next_id(self) -> int:
        """Get the next available ID for a new person."""
        df = pd.read_csv(self.csv_path)
        if df.empty:
            return 1
        return df['id'].max() + 1
    
    def add_person(self, person_data: Dict[str, Any], face_encoding: List[float]) -> int:
        """
        Add a new person to the database.
        
        Args:
            person_data (Dict): Person details (name, class_name, roll_number, etc.)
            face_encoding (List[float]): Face encoding from face_recognition library
            
        Returns:
            int: ID of the added person
        """
        # Get next ID
        person_id = self.get_next_id()
        person_data['id'] = person_id
        
        # Add to CSV
        df = pd.read_csv(self.csv_path)
        new_row = pd.DataFrame([person_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.csv_path, index=False)
        
        # Add encoding
        self.encodings[person_id] = face_encoding
        self._save_encodings()
        
        return person_id
    
    def get_person_by_id(self, person_id: int) -> Optional[Dict[str, Any]]:
        """Get person details by ID."""
        df = pd.read_csv(self.csv_path)
        person = df[df['id'] == person_id]
        if not person.empty:
            return person.iloc[0].to_dict()
        return None
    
    def get_all_encodings(self) -> tuple:
        """
        Get all face encodings and corresponding person IDs.
        
        Returns:
            tuple: (encodings_list, person_ids_list)
        """
        encodings_list = []
        person_ids = []
        
        for person_id, encoding in self.encodings.items():
            encodings_list.append(encoding)
            person_ids.append(person_id)
        
        return encodings_list, person_ids
    
    def get_person_count(self) -> int:
        """Get total number of registered persons."""
        return len(self.encodings)
    
    def capture_face_encoding(self, image_path: str = None, webcam_capture: bool = True) -> Optional[List[float]]:
        """
        Capture face encoding from image or webcam.
        
        Args:
            image_path (str): Path to image file (if not using webcam)
            webcam_capture (bool): Whether to capture from webcam
            
        Returns:
            List[float]: Face encoding or None if no face found
        """
        if webcam_capture:
            return self._capture_from_webcam()
        else:
            return self._capture_from_image(image_path)
    
    def _capture_from_webcam(self) -> Optional[List[float]]:
        """Capture face encoding from webcam."""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return None
        
        print("Press SPACE to capture face, ESC to cancel")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from webcam")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find face locations
            face_locations = face_recognition.face_locations(frame)
            
            if face_locations:
                # Draw rectangle around face
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Add instruction text
                cv2.putText(frame, "Face detected! Press SPACE to capture", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No face detected. Position yourself in front of camera", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.putText(frame, "Press SPACE to capture, ESC to cancel", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Face Capture', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space key
                if face_locations:
                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(frame, face_locations)
                    if face_encodings:
                        cap.release()
                        cv2.destroyAllWindows()
                        return face_encodings[0]
                    else:
                        print("Could not generate face encoding. Try again.")
                else:
                    print("No face detected. Please position yourself in front of the camera.")
            elif key == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return None
    
    def _capture_from_image(self, image_path: str) -> Optional[List[float]]:
        """Capture face encoding from image file."""
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return None
        
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Find face locations
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            print("No face found in the image")
            return None
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if face_encodings:
            return face_encodings[0]
        else:
            print("Could not generate face encoding from image")
            return None


def test_data_manager():
    """Test function for DataManager class."""
    dm = DataManager()
    print(f"Data directory: {dm.data_dir}")
    print(f"CSV path: {dm.csv_path}")
    print(f"Encodings path: {dm.encodings_path}")
    print(f"Current person count: {dm.get_person_count()}")


if __name__ == "__main__":
    test_data_manager()

