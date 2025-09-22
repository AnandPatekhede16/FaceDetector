"""
Simplified Data Management for Face Recognition System
Handles CSV storage for person details and pickle storage for face encodings.
"""

import pandas as pd
import pickle
import os
from typing import List, Dict, Any, Optional
import face_recognition
import cv2
import numpy as np


class SimpleDataManager:
    """Simplified data manager for face recognition system."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize SimpleDataManager with data directory."""
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
            try:
                with open(self.encodings_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading encodings: {e}")
                return {}
        return {}
    
    def _save_encodings(self):
        """Save face encodings to pickle file."""
        try:
            with open(self.encodings_path, 'wb') as f:
                pickle.dump(self.encodings, f)
        except Exception as e:
            print(f"Error saving encodings: {e}")
    
    def get_next_id(self) -> int:
        """Get the next available ID for a new person."""
        try:
            df = pd.read_csv(self.csv_path)
            if df.empty:
                return 1
            return df['id'].max() + 1
        except Exception as e:
            print(f"Error getting next ID: {e}")
            return 1
    
    def add_person(self, person_data: Dict[str, Any], face_encoding: List[float]) -> int:
        """Add a new person to the database."""
        try:
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
        except Exception as e:
            print(f"Error adding person: {e}")
            return -1
    
    def get_person_by_id(self, person_id: int) -> Optional[Dict[str, Any]]:
        """Get person details by ID."""
        try:
            df = pd.read_csv(self.csv_path)
            person = df[df['id'] == person_id]
            if not person.empty:
                return person.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error getting person by ID: {e}")
            return None
    
    def get_all_encodings(self) -> tuple:
        """Get all face encodings and corresponding person IDs."""
        try:
            encodings_list = []
            person_ids = []
            
            for person_id, encoding in self.encodings.items():
                encodings_list.append(encoding)
                person_ids.append(person_id)
            
            return encodings_list, person_ids
        except Exception as e:
            print(f"Error getting all encodings: {e}")
            return [], []
    
    def get_person_count(self) -> int:
        """Get total number of registered persons."""
        return len(self.encodings)
    
    def test_camera(self, camera_index=0):
        """Test if camera is working."""
        cap = None
        try:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                return False
            
            ret, frame = cap.read()
            if not ret:
                return False
            
            return True
        except Exception as e:
            print(f"Camera test error: {e}")
            return False
        finally:
            if cap is not None:
                cap.release()


def test_simple_data_manager():
    """Test function for SimpleDataManager class."""
    try:
        dm = SimpleDataManager()
        print(f"✓ Data directory: {dm.data_dir}")
        print(f"✓ CSV path: {dm.csv_path}")
        print(f"✓ Encodings path: {dm.encodings_path}")
        print(f"✓ Current person count: {dm.get_person_count()}")
        
        # Test camera
        for i in range(3):
            if dm.test_camera(i):
                print(f"✓ Camera {i} is working")
                break
        else:
            print("✗ No working camera found")
        
        return True
    except Exception as e:
        print(f"✗ DataManager test failed: {e}")
        return False


if __name__ == "__main__":
    test_simple_data_manager()

