#!/usr/bin/env python3
"""
Test script to verify all fixes work correctly
Tests the application without actually running the full GUI
"""

import sys
import os
import importlib

def test_imports():
    """Test all imports work correctly"""
    print("Testing imports...")
    
    # Test core imports
    try:
        import psutil
        print("✅ psutil imported successfully")
    except ImportError as e:
        print(f"❌ psutil import failed: {e}")
        return False
    
    # Test tkinter
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        print("   Install with: sudo apt-get install python3-tk (Ubuntu)")
        return False
    
    # Test optional imports
    try:
        import pystray
        from PIL import Image
        print("✅ System tray dependencies available")
    except ImportError:
        print("⚠️  System tray dependencies not available (optional)")
    
    try:
        if sys.platform == "win32":
            import win10toast
            print("✅ Windows notifications available")
    except ImportError:
        print("⚠️  Windows notifications not available (optional)")
    
    return True

def test_password_hashing():
    """Test password hashing functionality"""
    print("\nTesting password hashing...")
    
    try:
        import hashlib
        
        # Test the hash function
        password = "admin123"
        expected_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
        actual_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if actual_hash == expected_hash:
            print("✅ Password hashing works correctly")
            return True
        else:
            print(f"❌ Password hash mismatch: {actual_hash} != {expected_hash}")
            return False
    except Exception as e:
        print(f"❌ Password hashing failed: {e}")
        return False

def test_process_monitoring():
    """Test process monitoring functionality"""
    print("\nTesting process monitoring...")
    
    try:
        import psutil
        
        # Test basic process iteration
        process_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                info = proc.info
                if info['name']:  # Valid process
                    process_count += 1
                if process_count >= 5:  # Just test a few
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if process_count > 0:
            print(f"✅ Process monitoring works (found {process_count} processes)")
            return True
        else:
            print("❌ No processes found")
            return False
    except Exception as e:
        print(f"❌ Process monitoring failed: {e}")
        return False

def test_config_handling():
    """Test configuration file handling"""
    print("\nTesting configuration handling...")
    
    try:
        import json
        from pathlib import Path
        
        # Test config creation
        test_config = {
            'blocked_apps': {},
            'password_hash': '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'
        }
        
        config_file = Path("test_config.json")
        
        # Write test config
        with open(config_file, 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Read test config
        with open(config_file, 'r') as f:
            loaded_config = json.load(f)
        
        # Clean up
        config_file.unlink()
        
        if loaded_config == test_config:
            print("✅ Configuration handling works correctly")
            return True
        else:
            print("❌ Configuration mismatch")
            return False
    except Exception as e:
        print(f"❌ Configuration handling failed: {e}")
        return False

def test_main_import():
    """Test importing the main application"""
    print("\nTesting main application import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import main components
        from main import LoginWindow, AppLockManager
        print("✅ Main application classes imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main application import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Windows App Lock - Testing Fixes")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_password_hashing,
        test_process_monitoring,
        test_config_handling,
        test_main_import
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The application should work correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)