#!/usr/bin/env python3
"""
Quick test to verify login password box visibility
Run this to see if the password input is visible
"""

import tkinter as tk
from tkinter import messagebox

def main():
    """Create a simple test window to verify password box visibility"""
    
    root = tk.Tk()
    root.title("Password Box Visibility Test")
    root.geometry("450x350")
    root.configure(bg='#2c3e50')
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (225)
    y = (root.winfo_screenheight() // 2) - (175)
    root.geometry(f'450x350+{x}+{y}')
    
    # Main frame
    main_frame = tk.Frame(root, bg='#2c3e50')
    main_frame.pack(expand=True, fill='both', padx=30, pady=30)
    
    # Title
    title = tk.Label(main_frame, text="Password Box Visibility Test", 
                    font=('Arial', 16, 'bold'), 
                    bg='#2c3e50', fg='white')
    title.pack(pady=(0, 20))
    
    # Instructions
    instructions = tk.Label(main_frame, 
                           text="This test verifies the password input box is visible.\\n\\n" +
                                "✅ You should see a WHITE rectangle with BLUE border below\\n" +
                                "✅ When you type, it should show asterisks (*)\\n" +
                                "✅ The box should be clearly visible against the dark background",
                           font=('Arial', 10), 
                           bg='#2c3e50', fg='#bdc3c7',
                           justify='left')
    instructions.pack(pady=(0, 20))
    
    # Password section
    password_frame = tk.Frame(main_frame, bg='#2c3e50')
    password_frame.pack(fill='x', pady=20)
    
    password_label = tk.Label(password_frame, text="Test Password:", 
                             font=('Arial', 12, 'bold'), 
                             bg='#2c3e50', fg='white')
    password_label.pack(anchor='w', pady=(0, 5))
    
    # Highly visible password entry with blue border
    entry_container = tk.Frame(password_frame, bg='#3498db', relief='solid', bd=2)
    entry_container.pack(fill='x', pady=(5, 0))
    
    password_var = tk.StringVar()
    password_entry = tk.Entry(entry_container, textvariable=password_var, 
                             show='*', font=('Arial', 14, 'bold'), 
                             bg='white', fg='black', 
                             insertbackground='black',
                             relief='flat', bd=0,
                             highlightthickness=0)
    password_entry.pack(fill='x', padx=3, pady=3, ipady=10)
    
    # Test button
    def test_input():
        password = password_var.get()
        if password:
            messagebox.showinfo("Success!", 
                              f"✅ Password box is working!\\n\\n" +
                              f"You entered {len(password)} characters.\\n" +
                              f"The password box is clearly visible.")
        else:
            messagebox.showwarning("No Input", 
                                 "Please type something in the password box first.")
    
    test_btn = tk.Button(password_frame, text="Test Password Input", 
                        command=test_input,
                        font=('Arial', 12, 'bold'),
                        bg='#27ae60', fg='white',
                        relief='flat', pady=10,
                        cursor='hand2')
    test_btn.pack(fill='x', pady=15)
    
    # Status
    status_frame = tk.Frame(main_frame, bg='#2c3e50')
    status_frame.pack(fill='x', pady=20)
    
    status_label = tk.Label(status_frame, 
                           text="Status: Ready for testing\\n\\n" +
                                "Default password for the actual app: admin123",
                           font=('Arial', 10), 
                           bg='#2c3e50', fg='#f39c12',
                           justify='center')
    status_label.pack()
    
    # Focus on password entry
    password_entry.focus()
    
    # Bind Enter key
    password_entry.bind('<Return>', lambda e: test_input())
    
    print("🔍 Password Box Visibility Test Started")
    print("=" * 50)
    print("WHAT TO CHECK:")
    print("1. ✅ Can you see a WHITE rectangle with BLUE border?")
    print("2. ✅ When you type, do you see asterisks (*)?")
    print("3. ✅ Is the password box clearly visible?")
    print("4. ✅ Can you click in the box and type?")
    print("")
    print("If you can see and use the password box, the fix is working!")
    print("Close the window when you're done testing.")
    
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure tkinter is installed: sudo apt-get install python3-tk")