"""
Test script to verify the face recognition system components.
"""

import os
import sys
from data_manager import DataManager


def test_data_manager():
    """Test the DataManager class functionality."""
    print("Testing DataManager...")
    
    try:
        # Initialize data manager
        dm = DataManager()
        print("✓ DataManager initialized successfully")
        
        # Test CSV initialization
        if os.path.exists(dm.csv_path):
            print("✓ CSV file created successfully")
        else:
            print("✗ CSV file not found")
            return False
        
        # Test encodings file
        if os.path.exists(dm.encodings_path):
            print("✓ Encodings file exists")
        else:
            print("ℹ Encodings file will be created on first registration")
        
        # Test person count
        count = dm.get_person_count()
        print(f"✓ Current person count: {count}")
        
        return True
        
    except Exception as e:
        print(f"✗ DataManager test failed: {str(e)}")
        return False


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


def test_data_directory():
    """Test if data directory exists and is writable."""
    print("Testing data directory...")
    
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"✗ Data directory '{data_dir}' does not exist")
        return False
    
    if not os.path.isdir(data_dir):
        print(f"✗ '{data_dir}' is not a directory")
        return False
    
    # Test write permissions
    try:
        test_file = os.path.join(data_dir, "test_write.tmp")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✓ Data directory is writable")
        return True
    except Exception as e:
        print(f"✗ Data directory is not writable: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("FACE RECOGNITION SYSTEM - TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Directory Test", test_data_directory),
        ("DataManager Test", test_data_manager)
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
        print("1. Run 'python run.py' to start the system")
        print("2. Or run 'python register.py' to register faces")
        print("3. Or run 'python recognize.py' to start recognition")
    else:
        print("❌ Some tests failed. Please fix the issues before using the system.")
        print("\nCommon solutions:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check if webcam is available")
        print("3. Ensure you have write permissions in the current directory")


if __name__ == "__main__":
    main()

