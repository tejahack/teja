#!/usr/bin/env python3
"""
Minimal Windows App Lock - Works without external dependencies
This version demonstrates the core functionality without psutil, pystray, etc.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows App Lock - Login")
        self.root.geometry("400x300")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Default password hash (password: "admin123")
        self.password_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
        self.load_password()
        
        # Security features
        self.authenticated = False
        self.login_attempts = 0
        self.max_attempts = 3
        self.lockout_time = 30  # seconds
        self.locked_until = None
        
        self.setup_login_gui()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Focus on password entry
        self.root.after(100, lambda: self.password_entry.focus())
    
    def center_window(self):
        """Center the login window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_password(self):
        """Load password hash from config file"""
        config_file = Path("app_lock_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.password_hash = config.get('password_hash', self.password_hash)
            except Exception as e:
                print(f"Error loading password: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify password against stored hash"""
        return self.hash_password(password) == self.password_hash
    
    def setup_login_gui(self):
        """Setup the login GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Logo/Title section
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(pady=(0, 30))
        
        # App icon (using text as placeholder)
        icon_frame = tk.Frame(title_frame, bg='#e74c3c', width=60, height=60)
        icon_frame.pack(pady=(0, 15))
        icon_frame.pack_propagate(False)
        
        # Use a simple text icon that works across all systems
        icon_label = tk.Label(icon_frame, text="LOCK", font=('Arial', 10, 'bold'), 
                             bg='#e74c3c', fg='white')
        icon_label.pack(expand=True)
        
        # Title
        title_label = tk.Label(title_frame, text="Windows App Lock", 
                              font=('Arial', 18, 'bold'), 
                              bg='#2c3e50', fg='white')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Enter password to continue", 
                                 font=('Arial', 10), 
                                 bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(pady=(5, 0))
        
        # Login form
        form_frame = tk.Frame(main_frame, bg='#2c3e50')
        form_frame.pack(fill='x', pady=(0, 20))
        
        # Password field
        password_frame = tk.Frame(form_frame, bg='#2c3e50')
        password_frame.pack(fill='x', pady=(0, 15))
        
        password_label = tk.Label(password_frame, text="Password:", 
                                 font=('Arial', 11, 'bold'), 
                                 bg='#2c3e50', fg='white')
        password_label.pack(anchor='w', pady=(0, 5))
        
        # Create a container frame for better visibility
        entry_container = tk.Frame(password_frame, bg='#3498db', relief='solid', bd=1)
        entry_container.pack(fill='x', pady=(5, 0))
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(entry_container, textvariable=self.password_var, 
                                      show='*', font=('Arial', 12), 
                                      bg='white', fg='black', 
                                      insertbackground='black',
                                      relief='flat', bd=0,
                                      highlightthickness=0)
        self.password_entry.pack(fill='x', padx=2, pady=2, ipady=8)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = tk.Button(form_frame, text="Login", 
                             command=self.login,
                             font=('Arial', 12, 'bold'),
                             bg='#27ae60', fg='white',
                             relief='flat', bd=0,
                             cursor='hand2',
                             pady=10)
        login_btn.pack(fill='x', pady=(10, 0))
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(form_frame, textvariable=self.status_var,
                                    font=('Arial', 9),
                                    bg='#2c3e50', fg='#e74c3c')
        self.status_label.pack(pady=(10, 0))
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg='#2c3e50')
        footer_frame.pack(side='bottom', fill='x')
        
        footer_label = tk.Label(footer_frame, 
                               text="Default password: admin123\\nChange password in Settings after login",
                               font=('Arial', 8),
                               bg='#2c3e50', fg='#7f8c8d',
                               justify='center')
        footer_label.pack()
    
    def is_locked_out(self):
        """Check if currently locked out"""
        if self.locked_until and datetime.now() < self.locked_until:
            return True
        elif self.locked_until and datetime.now() >= self.locked_until:
            # Lockout period expired, reset
            self.locked_until = None
            self.login_attempts = 0
        return False
    
    def login(self):
        """Handle login attempt"""
        # Check if locked out
        if self.is_locked_out():
            remaining = int((self.locked_until - datetime.now()).total_seconds())
            self.status_var.set(f"Too many failed attempts. Try again in {remaining}s")
            return
        
        password = self.password_var.get()
        
        if not password:
            self.status_var.set("Please enter a password")
            return
        
        if self.verify_password(password):
            self.authenticated = True
            self.status_var.set("Login successful!")
            self.login_attempts = 0  # Reset attempts on success
            self.root.after(500, self.close_login)  # Close after brief delay
        else:
            self.login_attempts += 1
            remaining_attempts = self.max_attempts - self.login_attempts
            
            if self.login_attempts >= self.max_attempts:
                # Lock out for specified time
                self.locked_until = datetime.now() + timedelta(seconds=self.lockout_time)
                self.status_var.set(f"Too many failed attempts. Locked for {self.lockout_time}s")
                # Disable login controls temporarily
                self.password_entry.config(state='disabled')
                self.root.after(1000, self.update_lockout_status)
            else:
                self.status_var.set(f"Invalid password. {remaining_attempts} attempts remaining.")
            
            self.password_var.set("")  # Clear password field
            if self.login_attempts < self.max_attempts:
                self.password_entry.focus()
    
    def update_lockout_status(self):
        """Update lockout status display"""
        if self.is_locked_out():
            remaining = int((self.locked_until - datetime.now()).total_seconds())
            if remaining > 0:
                self.status_var.set(f"Locked out. Try again in {remaining}s")
                self.root.after(1000, self.update_lockout_status)
            else:
                self.status_var.set("Lockout expired. You may try again.")
                self.password_entry.config(state='normal')
                self.password_entry.focus()
        else:
            self.password_entry.config(state='normal')
            self.password_entry.focus()
    
    def close_login(self):
        """Close login window"""
        self.root.destroy()
    
    def on_closing(self):
        """Handle window close event"""
        self.root.destroy()
        sys.exit(0)  # Exit if login window is closed
    
    def run(self):
        """Run the login window"""
        self.root.mainloop()
        return self.authenticated

class MinimalAppLockManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows App Lock Manager (Minimal)")
        self.root.geometry("600x400")
        self.root.configure(bg='#2c3e50')
        
        # Configuration file path
        self.config_file = Path("app_lock_config.json")
        self.blocked_apps = {}
        self.monitoring = False
        
        # Default password hash (password: "admin123")
        self.password_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
        
        self.load_config()
        self.setup_gui()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify password against stored hash"""
        return self.hash_password(password) == self.password_hash
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.blocked_apps = config.get('blocked_apps', {})
                    self.password_hash = config.get('password_hash', self.password_hash)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        config = {
            'blocked_apps': self.blocked_apps,
            'password_hash': self.password_hash
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def setup_gui(self):
        """Setup the main GUI"""
        # Main title
        title_label = tk.Label(self.root, text="Windows App Lock Manager (Minimal)", 
                              font=('Arial', 16, 'bold'), 
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=20)
        
        # Info label
        info_label = tk.Label(self.root, 
                             text="This is a minimal version for demonstration.\\nFull functionality requires psutil and other dependencies.",
                             font=('Arial', 10), 
                             bg='#2c3e50', fg='#bdc3c7',
                             justify='center')
        info_label.pack(pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg='#2c3e50')
        btn_frame.pack(pady=20)
        
        # Demo buttons
        tk.Button(btn_frame, text="Show Blocked Apps", 
                 command=self.show_blocked_apps,
                 bg='#3498db', fg='white', 
                 font=('Arial', 12), pady=10, padx=20).pack(pady=5, fill='x')
        
        tk.Button(btn_frame, text="Change Password", 
                 command=self.change_password,
                 bg='#e67e22', fg='white', 
                 font=('Arial', 12), pady=10, padx=20).pack(pady=5, fill='x')
        
        tk.Button(btn_frame, text="Exit", 
                 command=self.quit_app,
                 bg='#e74c3c', fg='white', 
                 font=('Arial', 12), pady=10, padx=20).pack(pady=5, fill='x')
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Minimal Mode")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bg='#34495e', fg='white', relief='sunken')
        status_bar.pack(side='bottom', fill='x')
    
    def show_blocked_apps(self):
        """Show blocked applications"""
        if not self.blocked_apps:
            messagebox.showinfo("Blocked Apps", "No applications are currently blocked.")
        else:
            apps_list = "\\n".join([f"• {config['name']}" for config in self.blocked_apps.values()])
            messagebox.showinfo("Blocked Apps", f"Currently blocked applications:\\n\\n{apps_list}")
    
    def change_password(self):
        """Change password dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Password")
        dialog.geometry("300x200")
        dialog.configure(bg='#2c3e50')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (150)
        y = (dialog.winfo_screenheight() // 2) - (100)
        dialog.geometry(f'300x200+{x}+{y}')
        
        # Current password
        tk.Label(dialog, text="Current Password:", bg='#2c3e50', fg='white').pack(pady=5)
        current_var = tk.StringVar()
        current_entry = tk.Entry(dialog, textvariable=current_var, show='*', 
                                bg='white', fg='black', insertbackground='black',
                                relief='solid', bd=2)
        current_entry.pack(pady=5, padx=20, fill='x')
        
        # New password
        tk.Label(dialog, text="New Password:", bg='#2c3e50', fg='white').pack(pady=5)
        new_var = tk.StringVar()
        new_entry = tk.Entry(dialog, textvariable=new_var, show='*', 
                            bg='white', fg='black', insertbackground='black',
                            relief='solid', bd=2)
        new_entry.pack(pady=5, padx=20, fill='x')
        
        def save_password():
            if not self.verify_password(current_var.get()):
                messagebox.showerror("Error", "Current password is incorrect", parent=dialog)
                return
            
            if len(new_var.get()) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters", parent=dialog)
                return
            
            self.password_hash = self.hash_password(new_var.get())
            self.save_config()
            messagebox.showinfo("Success", "Password changed successfully", parent=dialog)
            dialog.destroy()
        
        tk.Button(dialog, text="Change Password", command=save_password,
                 bg='#27ae60', fg='white').pack(pady=10)
    
    def quit_app(self):
        """Quit the application"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("Windows App Lock - Minimal Version")
    print("This version works without psutil and system tray dependencies")
    print("Default password: admin123")
    print()
    
    # Show login window first
    login_window = LoginWindow()
    authenticated = login_window.run()
    
    # Only proceed if authentication was successful
    if authenticated:
        print("Authentication successful. Starting main application...")
        app = MinimalAppLockManager()
        app.run()
    else:
        print("Authentication failed or cancelled. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()