# Face Detection + Recognition System

A complete face detection and recognition system built with Python, OpenCV, and face-recognition library. This system allows you to register people with their face encodings and then recognize them in real-time using a webcam.

## Features

### Registration System (`register.py`)
- Interactive form to capture person details (Name, Class, Roll Number, Email, Phone)
- Real-time face capture using webcam
- Face encoding generation and storage
- Data persistence using CSV and pickle files
- View registered persons

### Recognition System (`recognize.py`)
- Real-time face detection and recognition
- Live webcam feed with face identification
- Display person details (Name, Class, Roll Number) on video feed
- Confidence scoring for recognition accuracy
- Unknown person detection
- Performance optimizations (FPS display, frame skipping)

### Data Management (`data_manager.py`)
- Structured data storage (CSV for person details, pickle for face encodings)
- Automatic ID generation
- Face encoding capture from webcam or image files
- Data retrieval and management utilities

## Installation

1. **Clone or download the project files**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure you have a working webcam**

## Usage

### 1. Register New People

Run the registration system to add new people to the database:

```bash
python register.py
```

Follow the interactive prompts:
- Enter person details (Name, Class, Roll Number, etc.)
- Position yourself in front of the webcam
- Press SPACE when your face is detected to capture
- Press ESC to cancel

### 2. Recognize People

Run the recognition system for real-time face recognition:

```bash
python recognize.py
```

**Controls:**
- `q` - Quit the recognition system
- `r` - Reload registered faces
- `t` - Toggle recognition tolerance (0.6/0.9)

### 3. View Registered People

From the registration menu, select option 2 to view all registered people.

## File Structure

```
demo/
├── data/                          # Data storage directory
│   ├── person_details.csv        # Person details (CSV)
│   └── face_encodings.pkl        # Face encodings (pickle)
├── data_manager.py               # Data management utilities
├── register.py                   # Registration system
├── recognize.py                  # Recognition system
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Technical Details

### Dependencies
- `opencv-python` - Computer vision and webcam handling
- `face-recognition` - Face detection and encoding
- `numpy` - Numerical operations
- `pandas` - Data manipulation and CSV handling
- `Pillow` - Image processing

### Data Storage
- **CSV File**: Stores person details (ID, Name, Class, Roll Number, Email, Phone, Registration Date)
- **Pickle File**: Stores face encodings as numpy arrays for fast retrieval

### Performance Optimizations
- Frame resizing for faster processing
- Frame skipping (process every other frame)
- Efficient face encoding comparison
- Real-time FPS monitoring

### Recognition Accuracy
- Configurable tolerance levels (0.6 = strict, 0.9 = lenient)
- Confidence scoring for each recognition
- Multiple face detection support

## Troubleshooting

### Common Issues

1. **"No registered faces found"**
   - Run `register.py` first to add some faces
   - Ensure the `data/` directory exists and contains files

2. **Webcam not working**
   - Check if webcam is connected and not used by other applications
   - Try changing the camera index in the code (0, 1, 2, etc.)

3. **Poor recognition accuracy**
   - Ensure good lighting conditions
   - Register faces with clear, front-facing images
   - Adjust tolerance level using 't' key in recognition mode

4. **Installation issues**
   - Make sure you have Python 3.7+ installed
   - Use `pip install --upgrade pip` before installing requirements
   - On Windows, you might need Visual C++ Build Tools for some packages

### Performance Tips

- Use good lighting for both registration and recognition
- Register multiple angles of the same person for better accuracy
- Close other applications using the webcam
- Adjust tolerance based on your needs (lower = more strict)

## Customization

### Adding New Fields
To add new person details, modify the `_init_csv()` method in `data_manager.py` and update the registration form in `register.py`.

### Changing Recognition Tolerance
Modify the `tolerance` parameter in the `FaceRecognizer` class initialization in `recognize.py`.

### Using Different Camera
Change the camera index in the `cv2.VideoCapture(0)` calls to use a different camera (0, 1, 2, etc.).

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please check the troubleshooting section above or create an issue in the project repository.

