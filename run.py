"""
Main launcher script for the Face Recognition System.
Provides a simple menu to access registration and recognition modules.
"""

import os
import sys


def print_banner():
    """Print the system banner."""
    print("=" * 60)
    print("    FACE DETECTION + RECOGNITION SYSTEM")
    print("=" * 60)
    print("    Built with Python + OpenCV + face-recognition")
    print("=" * 60)


def check_dependencies():
    """Check if required dependencies are installed."""
    required_modules = ['cv2', 'face_recognition', 'numpy', 'pandas']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Missing required dependencies:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\nPlease install dependencies using:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Main function to run the system launcher."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\nExiting...")
        return
    
    print("✅ All dependencies are installed!")
    print()
    
    while True:
        try:
            print("MAIN MENU")
            print("-" * 20)
            print("1. Register new person")
            print("2. Start face recognition")
            print("3. View registered persons")
            print("4. Install/Update dependencies")
            print("5. Exit")
            print("-" * 20)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                print("\nStarting registration system...")
                os.system("python register.py")
            
            elif choice == '2':
                print("\nStarting face recognition system...")
                os.system("python recognize.py")
            
            elif choice == '3':
                print("\nViewing registered persons...")
                os.system("python -c \"from data_manager import DataManager; dm = DataManager(); import pandas as pd; df = pd.read_csv(dm.csv_path); print('\\nRegistered Persons:'); print(df.to_string(index=False)) if not df.empty else print('No persons registered yet.')")
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                print("\nInstalling/Updating dependencies...")
                os.system("pip install -r requirements.txt")
                print("Dependencies installation completed!")
                input("Press Enter to continue...")
            
            elif choice == '5':
                print("\nThank you for using the Face Recognition System!")
                break
            
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()

