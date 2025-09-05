#!/usr/bin/env python3
"""
Test script for the new password-before-open functionality
This demonstrates how the app prompts for password before allowing blocked apps to run
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time

class TestPasswordBeforeOpen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test: Password Before Open Feature")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup test GUI"""
        # Header
        header = tk.Label(self.root, text="Password Before Open - Feature Test", 
                         font=('Arial', 16, 'bold'), 
                         bg='#2c3e50', fg='white')
        header.pack(pady=20)
        
        # Description
        desc_text = """This test demonstrates the new password-before-open feature:

🔒 FEATURE OVERVIEW:
• When a blocked application tries to start, it's paused (not killed)
• A password dialog appears asking for permission
• With correct password: App gets 5-minute temporary access
• With wrong password: App is terminated
• Failed attempts are logged and tracked

🎯 HOW IT WORKS:
1. App monitoring detects blocked application
2. Process is suspended (paused)
3. Password dialog appears
4. User can grant temporary access or deny
5. All attempts are logged for security

🔐 SECURITY FEATURES:
• 3 failed attempts = automatic denial
• 30-second auto-timeout on dialog
• All access attempts logged
• Temporary access expires automatically
• Failed attempts tracked per application"""
        
        desc_label = tk.Label(self.root, text=desc_text, 
                             font=('Arial', 10), 
                             bg='#2c3e50', fg='#bdc3c7',
                             justify='left')
        desc_label.pack(pady=20, padx=30, fill='x')
        
        # Demo section
        demo_frame = tk.LabelFrame(self.root, text="Demo Controls", 
                                  bg='#34495e', fg='white',
                                  font=('Arial', 12, 'bold'))
        demo_frame.pack(fill='x', padx=30, pady=20)
        
        # Simulate blocked app button
        simulate_btn = tk.Button(demo_frame, text="🚫 Simulate Blocked App Launch", 
                               command=self.simulate_blocked_app,
                               bg='#e74c3c', fg='white', 
                               font=('Arial', 12, 'bold'),
                               relief='flat', pady=10)
        simulate_btn.pack(fill='x', padx=20, pady=10)
        
        # Show access dialog button
        dialog_btn = tk.Button(demo_frame, text="🔐 Show Password Dialog", 
                             command=self.show_demo_dialog,
                             bg='#f39c12', fg='white', 
                             font=('Arial', 12, 'bold'),
                             relief='flat', pady=10)
        dialog_btn.pack(fill='x', padx=20, pady=10)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready for testing...")
        status_label = tk.Label(self.root, textvariable=self.status_var,
                               font=('Arial', 10, 'bold'),
                               bg='#2c3e50', fg='#f39c12')
        status_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="💡 TIP: Try entering wrong passwords to see the security features!\nDefault password: admin123",
                               font=('Arial', 9),
                               bg='#2c3e50', fg='#95a5a6',
                               justify='center')
        instructions.pack(pady=10)
    
    def simulate_blocked_app(self):
        """Simulate a blocked application trying to start"""
        self.status_var.set("🚫 Blocked app detected! Showing password dialog...")
        
        # Simulate the real behavior
        app_config = {
            'name': 'Test Application',
            'path': '/fake/path/testapp.exe'
        }
        
        # Show the access dialog after a short delay
        self.root.after(1000, lambda: self.show_access_dialog(app_config))
    
    def show_demo_dialog(self):
        """Show the password dialog directly"""
        app_config = {
            'name': 'Demo Application',
            'path': '/demo/path/demoapp.exe'
        }
        self.show_access_dialog(app_config)
    
    def show_access_dialog(self, app_config):
        """Show the actual access dialog (simplified version)"""
        # Create modal dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Application Access Request")
        dialog.geometry("400x280")
        dialog.configure(bg='#2c3e50')
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (200)
        y = (dialog.winfo_screenheight() // 2) - (140)
        dialog.geometry(f'400x280+{x}+{y}')
        
        # Header
        header_frame = tk.Frame(dialog, bg='#e74c3c')
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="⚠️ BLOCKED APPLICATION", 
                font=('Arial', 12, 'bold'), 
                bg='#e74c3c', fg='white').pack(pady=12)
        
        # Content
        content_frame = tk.Frame(dialog, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=25, pady=20)
        
        # App info
        app_info = tk.Label(content_frame, 
                           text=f"Application: {app_config['name']}\\n\\nThis application is currently blocked.\\nEnter password to grant temporary access (5 minutes):",
                           font=('Arial', 10), 
                           bg='#2c3e50', fg='white',
                           justify='center')
        app_info.pack(pady=(0, 20))
        
        # Password section
        password_frame = tk.Frame(content_frame, bg='#2c3e50')
        password_frame.pack(fill='x', pady=10)
        
        tk.Label(password_frame, text="Password:", 
                font=('Arial', 11, 'bold'), 
                bg='#2c3e50', fg='white').pack(anchor='w')
        
        # Password entry with blue border
        entry_container = tk.Frame(password_frame, bg='#3498db', relief='solid', bd=1)
        entry_container.pack(fill='x', pady=(8, 0))
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(entry_container, textvariable=password_var, 
                                 show='*', font=('Arial', 11),
                                 bg='white', fg='black',
                                 insertbackground='black',
                                 relief='flat', bd=0,
                                 highlightthickness=0)
        password_entry.pack(fill='x', padx=2, pady=2, ipady=8)
        
        # Status
        status_var = tk.StringVar()
        status_label = tk.Label(password_frame, textvariable=status_var,
                               font=('Arial', 9),
                               bg='#2c3e50', fg='#e74c3c')
        status_label.pack(pady=(8, 0))
        
        # Attempt counter
        attempts = {'count': 0}
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#2c3e50')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        def grant_access():
            password = password_var.get()
            if not password:
                status_var.set("Please enter a password")
                return
            
            if password == "admin123":  # Demo password
                messagebox.showinfo("Access Granted!", 
                                  f"✅ Temporary access granted to {app_config['name']}\\n\\nAccess will expire in 5 minutes.")
                self.status_var.set(f"✅ Access granted to {app_config['name']} for 5 minutes")
                dialog.destroy()
            else:
                attempts['count'] += 1
                if attempts['count'] >= 3:
                    status_var.set("Too many failed attempts. Access denied.")
                    messagebox.showerror("Access Denied", 
                                       f"❌ Too many failed attempts!\\n\\n{app_config['name']} has been blocked.")
                    self.status_var.set(f"❌ Access denied to {app_config['name']} - too many failed attempts")
                    self.root.after(2000, dialog.destroy)
                    return
                
                status_var.set(f"Invalid password. Attempt {attempts['count']}/3")
                password_var.set("")
                password_entry.focus()
        
        def deny_access():
            messagebox.showinfo("Access Denied", f"❌ Access denied to {app_config['name']}")
            self.status_var.set(f"❌ Access denied to {app_config['name']}")
            dialog.destroy()
        
        # Buttons
        tk.Button(btn_frame, text="Grant Access (5 min)", 
                 command=grant_access,
                 bg='#27ae60', fg='white', 
                 font=('Arial', 11, 'bold'),
                 relief='flat', pady=10).pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        tk.Button(btn_frame, text="Deny Access", 
                 command=deny_access,
                 bg='#e74c3c', fg='white', 
                 font=('Arial', 11, 'bold'),
                 relief='flat', pady=10).pack(side='right', fill='x', expand=True, padx=(8, 0))
        
        # Focus and bindings
        password_entry.bind('<Return>', lambda e: grant_access())
        password_entry.focus()
        
        # Auto-timeout demo
        def auto_timeout():
            if dialog.winfo_exists():
                status_var.set("Dialog timed out - access denied")
                self.root.after(1500, dialog.destroy)
        
        dialog.after(30000, auto_timeout)  # 30 second timeout
    
    def run(self):
        """Run the test application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("Password Before Open - Feature Test")
    print("=" * 50)
    print("This demonstrates the new security feature:")
    print("• Blocked apps trigger password dialogs")
    print("• Correct password grants temporary access")
    print("• Wrong password blocks the application")
    print("• All attempts are logged and tracked")
    print("")
    print("Test password: admin123")
    print("")
    
    app = TestPasswordBeforeOpen()
    app.run()

if __name__ == "__main__":
    main()