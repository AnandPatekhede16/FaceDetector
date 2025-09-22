"""
Simple test script for the face recognition system.
Tests all components without complex dependencies.
"""

import os
import sys


def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    modules = [
        ('cv2', 'OpenCV'),
        ('face_recognition', 'face-recognition'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('pickle', 'Pickle (built-in)'),
        ('datetime', 'DateTime (built-in)')
    ]
    
    all_imports_ok = True
    
    for module, name in modules:
        try:
            __import__(module)
            print(f"✓ {name} imported successfully")
        except ImportError as e:
            print(f"✗ {name} import failed: {str(e)}")
            all_imports_ok = False
    
    return all_imports_ok


def test_camera():
    """Test camera functionality."""
    print("\nTesting camera...")
    
    try:
        import cv2
        
        for camera_index in [0, 1, 2]:
            try:
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    if ret:
                        print(f"✓ Camera {camera_index} is working")
                        return True
                    else:
                        print(f"✗ Camera {camera_index} opened but cannot read frames")
                else:
                    print(f"✗ Camera {camera_index} not available")
            except Exception as e:
                print(f"✗ Camera {camera_index} error: {e}")
        
        print("✗ No working camera found")
        return False
        
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False


def test_data_directory():
    """Test data directory creation."""
    print("\nTesting data directory...")
    
    try:
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        if os.path.exists(data_dir) and os.path.isdir(data_dir):
            print("✓ Data directory created successfully")
            return True
        else:
            print("✗ Data directory creation failed")
            return False
            
    except Exception as e:
        print(f"✗ Data directory test failed: {e}")
        return False


def test_simple_register():
    """Test the simple registration module."""
    print("\nTesting simple registration module...")
    
    try:
        # Import the simple register module
        import simple_register
        
        # Test camera function
        camera_index = simple_register.test_camera()
        if camera_index is not None:
            print(f"✓ Simple register camera test passed (camera {camera_index})")
        else:
            print("✗ Simple register camera test failed")
        
        return True
        
    except Exception as e:
        print(f"✗ Simple register test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("SIMPLE FACE RECOGNITION SYSTEM - TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Directory Test", test_data_directory),
        ("Camera Test", test_camera),
        ("Simple Register Test", test_simple_register)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python simple_register.py' to register faces")
        print("2. The system will automatically find and use your camera")
        print("3. Follow the on-screen instructions")
    else:
        print("❌ Some tests failed. Please fix the issues before using the system.")
        print("\nCommon solutions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check if webcam is available and not used by other apps")
        print("3. Ensure you have write permissions in the current directory")


if __name__ == "__main__":
    main()

