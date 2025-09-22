"""
Simple launcher for the Face Recognition System.
Provides easy access to all system components.
"""

import os
import sys


def print_banner():
    """Print the system banner."""
    print("=" * 60)
    print("    SIMPLE FACE RECOGNITION SYSTEM")
    print("=" * 60)
    print("    Error-Free Version with Improved Camera Handling")
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


def run_test():
    """Run the test suite."""
    print("Running system tests...")
    os.system("python test_simple.py")


def run_registration():
    """Run the registration system."""
    print("Starting registration system...")
    os.system("python simple_register.py")


def run_recognition():
    """Run the recognition system."""
    print("Starting recognition system...")
    os.system("python recognize.py")


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
            print("SIMPLE FACE RECOGNITION SYSTEM")
            print("-" * 40)
            print("1. Test system components")
            print("2. Register new person (Simple)")
            print("3. Register new person (Advanced)")
            print("4. Start face recognition")
            print("5. View registered persons")
            print("6. Install/Update dependencies")
            print("7. Exit")
            print("-" * 40)
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                run_test()
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                run_registration()
            
            elif choice == '3':
                print("Starting advanced registration system...")
                os.system("python register.py")
            
            elif choice == '4':
                run_recognition()
            
            elif choice == '5':
                print("Viewing registered persons...")
                os.system("python -c \"import simple_register; simple_register.view_registered_persons()\"")
                input("\nPress Enter to continue...")
            
            elif choice == '6':
                print("Installing/Updating dependencies...")
                os.system("pip install -r requirements.txt")
                print("Dependencies installation completed!")
                input("Press Enter to continue...")
            
            elif choice == '7':
                print("\nThank you for using the Face Recognition System!")
                break
            
            else:
                print("Invalid choice. Please enter 1-7.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()

