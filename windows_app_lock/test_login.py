"""
Test script for the login functionality
Run this to test the login window without starting the full application
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import LoginWindow

def test_login():
    """Test the login window"""
    print("Testing login window...")
    print("Default password: admin123")
    print("Try entering wrong passwords to test lockout feature")
    
    login = LoginWindow()
    authenticated = login.run()
    
    if authenticated:
        print("✅ Login successful!")
        return True
    else:
        print("❌ Login failed or cancelled")
        return False

if __name__ == "__main__":
    success = test_login()
    if success:
        print("Login test completed successfully")
    else:
        print("Login test failed")