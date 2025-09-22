"""
Face Registration Module
Captures face images and stores person details with face encodings.
"""

import cv2
import os
import sys
import numpy as np
import face_recognition
from datetime import datetime
from data_manager import DataManager


def get_person_details():
    """
    Get person details from user input.
    
    Returns:
        dict: Person details dictionary
    """
    print("\n" + "="*50)
    print("FACE REGISTRATION SYSTEM")
    print("="*50)
    
    person_data = {}
    
    # Get required details
    person_data['name'] = input("Enter Full Name: ").strip()
    if not person_data['name']:
        print("Error: Name is required!")
        return None
    
    person_data['class_name'] = input("Enter Class/Department: ").strip()
    if not person_data['class_name']:
        print("Error: Class/Department is required!")
        return None
    
    person_data['roll_number'] = input("Enter Roll Number/ID: ").strip()
    if not person_data['roll_number']:
        print("Error: Roll Number/ID is required!")
        return None
    
    # Get optional details
    person_data['email'] = input("Enter Email (optional): ").strip()
    person_data['phone'] = input("Enter Phone Number (optional): ").strip()
    
    # Add registration date
    person_data['registration_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return person_data


def display_person_details(person_data):
    """
    Display person details for confirmation.
    
    Args:
        person_data (dict): Person details dictionary
    """
    print("\n" + "-"*30)
    print("PERSON DETAILS SUMMARY")
    print("-"*30)
    print(f"Name: {person_data['name']}")
    print(f"Class/Department: {person_data['class_name']}")
    print(f"Roll Number/ID: {person_data['roll_number']}")
    print(f"Email: {person_data['email'] or 'Not provided'}")
    print(f"Phone: {person_data['phone'] or 'Not provided'}")
    print(f"Registration Date: {person_data['registration_date']}")
    print("-"*30)


def capture_face_encoding():
    """
    Capture face encoding using webcam with improved error handling.
    
    Returns:
        list: Face encoding or None if capture failed
    """
    print("\n" + "-"*30)
    print("FACE CAPTURE INSTRUCTIONS")
    print("-"*30)
    print("1. Position yourself in front of the camera")
    print("2. Ensure good lighting")
    print("3. Look directly at the camera")
    print("4. Press SPACE to capture when face is detected")
    print("5. Press ESC to cancel")
    print("-"*30)
    
    input("Press ENTER when ready to start face capture...")
    
    # Try to capture face encoding with multiple camera attempts
    face_encoding = None
    
    # Try different camera indices
    for camera_index in [0, 1, 2]:
        print(f"Trying camera index {camera_index}...")
        face_encoding = capture_from_webcam(camera_index)
        if face_encoding is not None:
            print("✓ Face captured successfully!")
            return face_encoding
    
    print("✗ Face capture failed. Please check your camera connection.")
    return None


def capture_from_webcam(camera_index=0):
    """
    Capture face encoding from webcam with specific camera index.
    
    Args:
        camera_index (int): Camera index to use
        
    Returns:
        list: Face encoding or None if capture failed
    """
    cap = None
    try:
        # Initialize camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            print(f"Camera {camera_index} not available")
            return None
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"Camera {camera_index} opened successfully!")
        print("Press SPACE to capture face, ESC to cancel")
        
        face_detected = False
        capture_attempts = 0
        max_attempts = 100  # Prevent infinite loop
        
        while capture_attempts < max_attempts:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find face locations
            face_locations = face_recognition.face_locations(frame)
            
            if face_locations:
                face_detected = True
                # Draw rectangle around face
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Add instruction text
                cv2.putText(frame, "Face detected! Press SPACE to capture", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                face_detected = False
                cv2.putText(frame, "No face detected. Position yourself in front of camera", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.putText(frame, "Press SPACE to capture, ESC to cancel", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Show frame
            cv2.imshow('Face Capture - Press SPACE to capture', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space key
                if face_locations:
                    try:
                        # Get face encodings
                        face_encodings = face_recognition.face_encodings(frame, face_locations)
                        if face_encodings and len(face_encodings) > 0:
                            print("Face encoding generated successfully!")
                            return face_encodings[0]
                        else:
                            print("Could not generate face encoding. Try again.")
                    except Exception as e:
                        print(f"Error generating face encoding: {str(e)}")
                        print("Try again with better lighting or different angle.")
                else:
                    print("No face detected. Please position yourself in front of the camera.")
            elif key == 27:  # ESC key
                print("Face capture cancelled by user")
                break
            
            capture_attempts += 1
        
        if capture_attempts >= max_attempts:
            print("Maximum capture attempts reached. Please try again.")
        
        return None
        
    except Exception as e:
        print(f"Error during face capture: {str(e)}")
        return None
    
    finally:
        # Clean up
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()


def register_person():
    """
    Main function to register a new person.
    """
    try:
        # Get person details
        person_data = get_person_details()
        if person_data is None:
            return False
        
        # Display details for confirmation
        display_person_details(person_data)
        
        # Confirm registration
        confirm = input("\nDo you want to proceed with registration? (y/n): ").lower().strip()
        if confirm != 'y':
            print("Registration cancelled.")
            return False
        
        # Capture face
        face_encoding = capture_face_encoding()
        if face_encoding is None:
            print("Registration failed: Could not capture face.")
            return False
        
        # Save to database
        dm = DataManager()
        person_id = dm.add_person(person_data, face_encoding)
        
        print(f"\n✓ Registration successful!")
        print(f"Person ID: {person_id}")
        print(f"Name: {person_data['name']}")
        print(f"Total registered persons: {dm.get_person_count()}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nRegistration cancelled by user.")
        return False
    except Exception as e:
        print(f"\nError during registration: {str(e)}")
        return False


def main():
    """
    Main function to run the registration system.
    """
    print("Welcome to Face Recognition Registration System!")
    
    while True:
        try:
            print("\n" + "="*50)
            print("REGISTRATION MENU")
            print("="*50)
            print("1. Register new person")
            print("2. View registered persons")
            print("3. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                success = register_person()
                if success:
                    print("\nRegistration completed successfully!")
                else:
                    print("\nRegistration failed. Please try again.")
            
            elif choice == '2':
                view_registered_persons()
            
            elif choice == '3':
                print("Thank you for using the Face Recognition System!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")


def view_registered_persons():
    """
    Display all registered persons.
    """
    try:
        dm = DataManager()
        
        if dm.get_person_count() == 0:
            print("\nNo persons registered yet.")
            return
        
        print(f"\nRegistered Persons (Total: {dm.get_person_count()})")
        print("-" * 80)
        print(f"{'ID':<5} {'Name':<20} {'Class':<15} {'Roll No':<15} {'Email':<20}")
        print("-" * 80)
        
        # Read CSV file
        import pandas as pd
        df = pd.read_csv(dm.csv_path)
        
        for _, row in df.iterrows():
            print(f"{row['id']:<5} {row['name']:<20} {row['class_name']:<15} {row['roll_number']:<15} {str(row['email']):<20}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error viewing registered persons: {str(e)}")


if __name__ == "__main__":
    main()
