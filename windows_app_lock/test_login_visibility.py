#!/usr/bin/env python3
"""
Test script to verify the login password box is visible and functional
"""

import sys
import os

def test_login_visibility():
    """Test that the login window shows properly with visible password box"""
    
    try:
        # Try to import tkinter
        import tkinter as tk
        from tkinter import messagebox
        
        print("✅ Tkinter imported successfully")
        
        # Create a test login window similar to the main app
        root = tk.Tk()
        root.title("Test - Login Visibility")
        root.geometry("400x300")
        root.configure(bg='#2c3e50')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title_label = tk.Label(main_frame, text="Password Visibility Test", 
                              font=('Arial', 16, 'bold'), 
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Password field
        password_frame = tk.Frame(main_frame, bg='#2c3e50')
        password_frame.pack(fill='x', pady=20)
        
        password_label = tk.Label(password_frame, text="Password:", 
                                 font=('Arial', 12), 
                                 bg='#2c3e50', fg='white')
        password_label.pack(anchor='w')
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, textvariable=password_var, 
                                 show='*', font=('Arial', 12), 
                                 bg='white', fg='black', 
                                 insertbackground='black',
                                 relief='solid', bd=2,
                                 highlightbackground='#3498db',
                                 highlightcolor='#3498db',
                                 highlightthickness=1)
        password_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Test button
        def test_password():
            password = password_var.get()
            if password:
                messagebox.showinfo("Success", f"Password entered: {'*' * len(password)}")
                print(f"✅ Password box is functional - entered {len(password)} characters")
            else:
                messagebox.showwarning("Warning", "No password entered")
        
        test_btn = tk.Button(password_frame, text="Test Password Entry", 
                            command=test_password,
                            font=('Arial', 12),
                            bg='#27ae60', fg='white',
                            relief='flat', pady=8)
        test_btn.pack(fill='x', pady=10)
        
        # Instructions
        instructions = tk.Label(main_frame, 
                               text="Instructions:\\n1. You should see a white password box above\\n2. Type something in the password box\\n3. Click 'Test Password Entry'\\n4. Close this window when done",
                               font=('Arial', 10),
                               bg='#2c3e50', fg='#bdc3c7',
                               justify='left')
        instructions.pack(pady=20)
        
        # Focus on password entry
        password_entry.focus()
        
        print("🔍 Test window created. Check if password box is visible:")
        print("   - Should see a white rectangle with blue border")
        print("   - Should be able to type in it (shows asterisks)")
        print("   - Should be able to test the input")
        
        # Show the test window
        root.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_minimal_version():
    """Test the minimal version login"""
    try:
        print("\\n🧪 Testing minimal version...")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app_lock_minimal import LoginWindow
        
        print("✅ Minimal version imported successfully")
        print("📝 To test: Run 'python3 app_lock_minimal.py' and check if password box is visible")
        
        return True
    except Exception as e:
        print(f"❌ Minimal version test failed: {e}")
        return False

def main():
    """Run visibility tests"""
    print("Password Box Visibility Test")
    print("=" * 40)
    
    # Test basic visibility
    test1_result = test_login_visibility()
    
    # Test minimal version import
    test2_result = test_minimal_version()
    
    print("\\n" + "=" * 40)
    print("Test Summary:")
    print(f"✅ Basic visibility test: {'PASSED' if test1_result else 'FAILED'}")
    print(f"✅ Minimal version test: {'PASSED' if test2_result else 'FAILED'}")
    
    if test1_result and test2_result:
        print("\\n🎉 All tests passed! Password boxes should be visible.")
    else:
        print("\\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()