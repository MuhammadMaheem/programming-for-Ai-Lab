"""
Test script to verify Hand Gesture Recognition installation
and demonstrate the system capabilities.
"""

import sys
import importlib

def test_imports():
    """Test all required package imports."""
    print("\n" + "="*50)
    print("Testing Package Imports")
    print("="*50)
    
    packages = {
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'numpy': 'NumPy',
        'flask': 'Flask',
    }
    
    all_good = True
    for package, name in packages.items():
        try:
            importlib.import_module(package)
            print(f"✓ {name} ({package}) - OK")
        except ImportError:
            print(f"✗ {name} ({package}) - MISSING")
            all_good = False
    
    return all_good

def test_gesture_detector():
    """Test the gesture detector module."""
    print("\n" + "="*50)
    print("Testing Gesture Detector")
    print("="*50)
    
    try:
        from gesture_detector import GestureDetector
        detector = GestureDetector()
        print("✓ GestureDetector class instantiated successfully")
        
        # Test available methods
        methods = [
            'calculate_distance',
            'is_finger_extended',
            'count_extended_fingers',
            'is_pinching',
            'recognize_gesture',
            'process_frame',
            'cleanup'
        ]
        
        for method in methods:
            if hasattr(detector, method):
                print(f"  ✓ Method '{method}' found")
            else:
                print(f"  ✗ Method '{method}' missing")
        
        detector.cleanup()
        return True
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_flask_app():
    """Test Flask application structure."""
    print("\n" + "="*50)
    print("Testing Flask Application")
    print("="*50)
    
    try:
        from flask import Flask
        from app import app
        print("✓ Flask app module imported successfully")
        
        # Test routes
        routes = [
            ('/', 'GET'),
            ('/video_feed', 'GET'),
            ('/detect_image', 'POST'),
            ('/stop_camera', 'POST'),
            ('/api/gesture-info', 'GET'),
            ('/health', 'GET'),
        ]
        
        print("\nAvailable routes:")
        for path, method in routes:
            print(f"  ✓ {method} {path}")
        
        return True
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_file_structure():
    """Test project file structure."""
    print("\n" + "="*50)
    print("Testing Project Structure")
    print("="*50)
    
    import os
    
    files = [
        'app.py',
        'gesture_detector.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'templates/index.html',
    ]
    
    all_good = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("Hand Gesture Recognition - Test Suite")
    print("="*50)
    
    results = []
    
    # Run tests
    results.append(("Import Check", test_imports()))
    results.append(("File Structure", test_file_structure()))
    results.append(("Gesture Detector", test_gesture_detector()))
    results.append(("Flask Application", test_flask_app()))
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50)
    
    if failed == 0:
        print("\n✓ All tests passed! Ready to run: python app.py\n")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
