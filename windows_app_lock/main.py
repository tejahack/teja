"""
Windows App Lock - Main Application
A comprehensive application to lock/block access to specific Windows applications
"""

# Import sys first
import sys

# Import handling with error checking
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
except ImportError:
    print("Error: tkinter is not available. This application requires tkinter.")
    print("On Ubuntu/Debian: sudo apt-get install python3-tk")
    print("On CentOS/RHEL: sudo yum install tkinter")
    print("On Windows: tkinter should be included with Python")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("Error: psutil is not installed. Run: pip install psutil")
    sys.exit(1)

import subprocess
import threading
import time
import json
import hashlib
import os
from datetime import datetime, timedelta
from pathlib import Path

# Optional imports with fallbacks
try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("Warning: System tray functionality not available (pystray/PIL not installed)")

try:
    if sys.platform == "win32":
        import win10toast
        NOTIFICATIONS_AVAILABLE = True
    else:
        NOTIFICATIONS_AVAILABLE = False
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

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
        try:
            icon_label = tk.Label(icon_frame, text="🔒", font=('Arial', 24), 
                                 bg='#e74c3c', fg='white')
        except:
            # Fallback for systems that don't support emoji
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
        
        # Show/Hide password checkbox
        self.show_password = tk.BooleanVar()
        show_cb = tk.Checkbutton(password_frame, text="Show password", 
                                variable=self.show_password,
                                command=self.toggle_password_visibility,
                                bg='#2c3e50', fg='#bdc3c7', 
                                selectcolor='#34495e',
                                activebackground='#2c3e50',
                                activeforeground='white')
        show_cb.pack(anchor='w', pady=(5, 0))
        
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
                               text="Default password: admin123\nChange password in Settings after login",
                               font=('Arial', 8),
                               bg='#2c3e50', fg='#7f8c8d',
                               justify='center')
        footer_label.pack()
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
    
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

class AppLockManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows App Lock Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Configuration file path
        self.config_file = Path("app_lock_config.json")
        self.blocked_apps = {}
        self.monitoring = False
        self.monitor_thread = None
        self.tray_icon = None
        
        # Default password hash (password: "admin123")
        self.password_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"
        
        self.load_config()
        self.setup_gui()
        self.start_monitoring()
        
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
        # Style configuration with error handling
        try:
            style = ttk.Style()
            # Try to use clam theme, fallback to default if not available
            try:
                style.theme_use('clam')
            except tk.TclError:
                print("Warning: 'clam' theme not available, using default theme")
            
            # Configure colors with error handling
            try:
                style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white')
                style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#2c3e50', foreground='white')
                style.configure('Custom.TFrame', background='#34495e')
            except tk.TclError as e:
                print(f"Warning: Could not configure custom styles: {e}")
        except Exception as e:
            print(f"Warning: Style configuration failed: {e}")
        
        # Main title
        title_label = ttk.Label(self.root, text="Windows App Lock Manager", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Blocked Apps Tab
        self.blocked_apps_frame = ttk.Frame(notebook)
        notebook.add(self.blocked_apps_frame, text="Blocked Applications")
        self.setup_blocked_apps_tab()
        
        # Running Processes Tab
        self.processes_frame = ttk.Frame(notebook)
        notebook.add(self.processes_frame, text="Running Processes")
        self.setup_processes_tab()
        
        # Settings Tab
        self.settings_frame = ttk.Frame(notebook)
        notebook.add(self.settings_frame, text="Settings")
        self.setup_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Monitoring: Active")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken')
        status_bar.pack(side='bottom', fill='x')
        
        # System tray setup (only if available)
        if TRAY_AVAILABLE:
            self.setup_system_tray()
        else:
            print("System tray functionality disabled (dependencies not available)")
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_blocked_apps_tab(self):
        """Setup the blocked applications tab"""
        # Header
        header_label = ttk.Label(self.blocked_apps_frame, text="Manage Blocked Applications", style='Heading.TLabel')
        header_label.pack(pady=10)
        
        # Add new app frame
        add_frame = ttk.LabelFrame(self.blocked_apps_frame, text="Add New Application to Block")
        add_frame.pack(fill='x', padx=20, pady=10)
        
        # App path entry
        path_frame = ttk.Frame(add_frame)
        path_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(path_frame, text="Application Path:").pack(side='left')
        self.app_path_var = tk.StringVar()
        self.app_path_entry = ttk.Entry(path_frame, textvariable=self.app_path_var, width=50)
        self.app_path_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_app)
        browse_btn.pack(side='right', padx=5)
        
        # App name entry
        name_frame = ttk.Frame(add_frame)
        name_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(name_frame, text="Display Name:").pack(side='left')
        self.app_name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.app_name_var, width=30).pack(side='left', padx=5)
        
        # Time restriction
        time_frame = ttk.Frame(add_frame)
        time_frame.pack(fill='x', padx=10, pady=5)
        
        self.time_restricted = tk.BooleanVar()
        ttk.Checkbutton(time_frame, text="Time Restricted", variable=self.time_restricted, 
                       command=self.toggle_time_restriction).pack(side='left')
        
        self.start_time_var = tk.StringVar(value="09:00")
        self.end_time_var = tk.StringVar(value="17:00")
        
        self.time_controls_frame = ttk.Frame(time_frame)
        self.time_controls_frame.pack(side='left', padx=20)
        
        ttk.Label(self.time_controls_frame, text="From:").grid(row=0, column=0, padx=5)
        ttk.Entry(self.time_controls_frame, textvariable=self.start_time_var, width=8).grid(row=0, column=1, padx=5)
        ttk.Label(self.time_controls_frame, text="To:").grid(row=0, column=2, padx=5)
        ttk.Entry(self.time_controls_frame, textvariable=self.end_time_var, width=8).grid(row=0, column=3, padx=5)
        
        # Initially hide time controls
        self.time_controls_frame.pack_forget()
        
        # Add button
        add_btn = ttk.Button(add_frame, text="Add Application", command=self.add_blocked_app)
        add_btn.pack(pady=10)
        
        # Blocked apps list
        list_frame = ttk.LabelFrame(self.blocked_apps_frame, text="Currently Blocked Applications")
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview for blocked apps
        columns = ('Name', 'Path', 'Status', 'Time Restriction')
        self.blocked_apps_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.blocked_apps_tree.heading(col, text=col)
            self.blocked_apps_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.blocked_apps_tree.yview)
        self.blocked_apps_tree.configure(yscrollcommand=scrollbar.set)
        
        self.blocked_apps_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Control buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_blocked_app).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_blocked_apps_list).pack(side='left', padx=5)
        
        self.refresh_blocked_apps_list()
    
    def setup_processes_tab(self):
        """Setup the running processes tab"""
        header_label = ttk.Label(self.processes_frame, text="Running Processes", style='Heading.TLabel')
        header_label.pack(pady=10)
        
        # Control frame
        control_frame = ttk.Frame(self.processes_frame)
        control_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Button(control_frame, text="Refresh Processes", command=self.refresh_processes).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Kill Selected Process", command=self.kill_selected_process).pack(side='left', padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.processes_frame)
        search_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(search_frame, text="Filter:").pack(side='left')
        self.process_filter_var = tk.StringVar()
        self.process_filter_var.trace('w', self.filter_processes)
        ttk.Entry(search_frame, textvariable=self.process_filter_var, width=30).pack(side='left', padx=5)
        
        # Processes list
        list_frame = ttk.Frame(self.processes_frame)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('PID', 'Name', 'CPU %', 'Memory %', 'Status')
        self.processes_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.processes_tree.heading(col, text=col)
            if col == 'PID':
                self.processes_tree.column(col, width=80)
            elif col in ['CPU %', 'Memory %']:
                self.processes_tree.column(col, width=100)
            else:
                self.processes_tree.column(col, width=150)
        
        scrollbar2 = ttk.Scrollbar(list_frame, orient='vertical', command=self.processes_tree.yview)
        self.processes_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.processes_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
        
        self.refresh_processes()
    
    def setup_settings_tab(self):
        """Setup the settings tab"""
        header_label = ttk.Label(self.settings_frame, text="Application Settings", style='Heading.TLabel')
        header_label.pack(pady=10)
        
        # Password settings
        password_frame = ttk.LabelFrame(self.settings_frame, text="Password Settings")
        password_frame.pack(fill='x', padx=20, pady=10)
        
        # Current password
        current_frame = ttk.Frame(password_frame)
        current_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(current_frame, text="Current Password:").pack(side='left')
        self.current_password_var = tk.StringVar()
        ttk.Entry(current_frame, textvariable=self.current_password_var, show='*', width=20).pack(side='left', padx=5)
        
        # New password
        new_frame = ttk.Frame(password_frame)
        new_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(new_frame, text="New Password:").pack(side='left')
        self.new_password_var = tk.StringVar()
        ttk.Entry(new_frame, textvariable=self.new_password_var, show='*', width=20).pack(side='left', padx=5)
        
        # Confirm password
        confirm_frame = ttk.Frame(password_frame)
        confirm_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(confirm_frame, text="Confirm Password:").pack(side='left')
        self.confirm_password_var = tk.StringVar()
        ttk.Entry(confirm_frame, textvariable=self.confirm_password_var, show='*', width=20).pack(side='left', padx=5)
        
        ttk.Button(password_frame, text="Change Password", command=self.change_password).pack(pady=10)
        
        # Monitoring settings
        monitoring_frame = ttk.LabelFrame(self.settings_frame, text="Monitoring Settings")
        monitoring_frame.pack(fill='x', padx=20, pady=10)
        
        self.auto_start = tk.BooleanVar()
        ttk.Checkbutton(monitoring_frame, text="Start monitoring on application launch", 
                       variable=self.auto_start).pack(anchor='w', padx=10, pady=5)
        
        self.minimize_to_tray = tk.BooleanVar(value=True)
        ttk.Checkbutton(monitoring_frame, text="Minimize to system tray", 
                       variable=self.minimize_to_tray).pack(anchor='w', padx=10, pady=5)
        
        self.show_notifications = tk.BooleanVar(value=True)
        ttk.Checkbutton(monitoring_frame, text="Show notifications when blocking apps", 
                       variable=self.show_notifications).pack(anchor='w', padx=10, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.settings_frame)
        control_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Button(control_frame, text="Save Settings", command=self.save_settings).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Export Config", command=self.export_config).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Import Config", command=self.import_config).pack(side='left', padx=5)
    
    def toggle_time_restriction(self):
        """Toggle time restriction controls"""
        if self.time_restricted.get():
            self.time_controls_frame.pack(side='left', padx=20)
        else:
            self.time_controls_frame.pack_forget()
    
    def browse_app(self):
        """Browse for application executable"""
        filename = filedialog.askopenfilename(
            title="Select Application",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.app_path_var.set(filename)
            # Auto-fill name if empty
            if not self.app_name_var.get():
                app_name = Path(filename).stem
                self.app_name_var.set(app_name)
    
    def add_blocked_app(self):
        """Add application to blocked list"""
        path = self.app_path_var.get().strip()
        name = self.app_name_var.get().strip()
        
        if not path or not name:
            messagebox.showerror("Error", "Please provide both application path and name")
            return
        
        if not os.path.exists(path):
            messagebox.showerror("Error", "Application path does not exist")
            return
        
        # Create app config
        app_config = {
            'name': name,
            'path': path,
            'time_restricted': self.time_restricted.get(),
            'start_time': self.start_time_var.get() if self.time_restricted.get() else None,
            'end_time': self.end_time_var.get() if self.time_restricted.get() else None,
            'blocked': True
        }
        
        self.blocked_apps[path] = app_config
        self.save_config()
        self.refresh_blocked_apps_list()
        
        # Clear form
        self.app_path_var.set("")
        self.app_name_var.set("")
        self.time_restricted.set(False)
        self.toggle_time_restriction()
        
        messagebox.showinfo("Success", f"Added {name} to blocked applications")
    
    def remove_blocked_app(self):
        """Remove selected application from blocked list"""
        selection = self.blocked_apps_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an application to remove")
            return
        
        item = self.blocked_apps_tree.item(selection[0])
        app_path = None
        
        # Find the app path by name
        for path, config in self.blocked_apps.items():
            if config['name'] == item['values'][0]:
                app_path = path
                break
        
        if app_path:
            del self.blocked_apps[app_path]
            self.save_config()
            self.refresh_blocked_apps_list()
            messagebox.showinfo("Success", "Application removed from blocked list")
    
    def refresh_blocked_apps_list(self):
        """Refresh the blocked applications list"""
        # Clear existing items
        for item in self.blocked_apps_tree.get_children():
            self.blocked_apps_tree.delete(item)
        
        # Add current blocked apps
        for path, config in self.blocked_apps.items():
            status = "Active" if config['blocked'] else "Inactive"
            time_restriction = "None"
            
            if config.get('time_restricted'):
                time_restriction = f"{config.get('start_time', '')} - {config.get('end_time', '')}"
            
            self.blocked_apps_tree.insert('', 'end', values=(
                config['name'],
                path,
                status,
                time_restriction
            ))
    
    def refresh_processes(self):
        """Refresh the running processes list"""
        try:
            # Clear existing items
            for item in self.processes_tree.get_children():
                self.processes_tree.delete(item)
            
            # Get processes with error handling
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    # Handle missing or None values
                    pid = info.get('pid', 'N/A')
                    name = info.get('name', 'Unknown')
                    cpu = info.get('cpu_percent', 0.0)
                    memory = info.get('memory_percent', 0.0)
                    status = info.get('status', 'Unknown')
                    
                    # Format values safely
                    cpu_str = f"{cpu:.1f}" if isinstance(cpu, (int, float)) else "0.0"
                    memory_str = f"{memory:.1f}" if isinstance(memory, (int, float)) else "0.0"
                    
                    self.processes_tree.insert('', 'end', values=(
                        pid, name, cpu_str, memory_str, status
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                except Exception as e:
                    print(f"Error processing individual process: {e}")
                    continue
        except Exception as e:
            print(f"Error refreshing processes: {e}")
            # Show error in status if available
            if hasattr(self, 'status_var'):
                self.status_var.set(f"Error refreshing processes: {str(e)[:50]}...")
    
    def filter_processes(self, *args):
        """Filter processes based on search term"""
        try:
            filter_text = self.process_filter_var.get().lower()
            
            # Clear and repopulate
            for item in self.processes_tree.get_children():
                self.processes_tree.delete(item)
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    name = info.get('name', 'Unknown')
                    
                    if filter_text in name.lower():
                        # Handle missing or None values
                        pid = info.get('pid', 'N/A')
                        cpu = info.get('cpu_percent', 0.0)
                        memory = info.get('memory_percent', 0.0)
                        status = info.get('status', 'Unknown')
                        
                        # Format values safely
                        cpu_str = f"{cpu:.1f}" if isinstance(cpu, (int, float)) else "0.0"
                        memory_str = f"{memory:.1f}" if isinstance(memory, (int, float)) else "0.0"
                        
                        self.processes_tree.insert('', 'end', values=(
                            pid, name, cpu_str, memory_str, status
                        ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                except Exception as e:
                    print(f"Error filtering individual process: {e}")
                    continue
        except Exception as e:
            print(f"Error filtering processes: {e}")
    
    def kill_selected_process(self):
        """Kill the selected process"""
        selection = self.processes_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process to kill")
            return
        
        item = self.processes_tree.item(selection[0])
        pid = int(item['values'][0])
        process_name = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to kill process '{process_name}' (PID: {pid})?"):
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                messagebox.showinfo("Success", f"Process {process_name} terminated")
                self.refresh_processes()
            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "Process no longer exists")
            except psutil.AccessDenied:
                messagebox.showerror("Error", "Access denied. Run as administrator to kill this process")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to kill process: {e}")
    
    def change_password(self):
        """Change the application password"""
        current = self.current_password_var.get()
        new_pass = self.new_password_var.get()
        confirm = self.confirm_password_var.get()
        
        if not self.verify_password(current):
            messagebox.showerror("Error", "Current password is incorrect")
            return
        
        if new_pass != confirm:
            messagebox.showerror("Error", "New passwords do not match")
            return
        
        if len(new_pass) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        self.password_hash = self.hash_password(new_pass)
        self.save_config()
        
        # Clear fields
        self.current_password_var.set("")
        self.new_password_var.set("")
        self.confirm_password_var.set("")
        
        messagebox.showinfo("Success", "Password changed successfully")
    
    def save_settings(self):
        """Save application settings"""
        self.save_config()
        messagebox.showinfo("Success", "Settings saved successfully")
    
    def export_config(self):
        """Export configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                config = {
                    'blocked_apps': self.blocked_apps,
                    'password_hash': self.password_hash
                }
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=2)
                messagebox.showinfo("Success", f"Configuration exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export configuration: {e}")
    
    def import_config(self):
        """Import configuration from file"""
        filename = filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                self.blocked_apps = config.get('blocked_apps', {})
                self.password_hash = config.get('password_hash', self.password_hash)
                
                self.save_config()
                self.refresh_blocked_apps_list()
                messagebox.showinfo("Success", f"Configuration imported from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import configuration: {e}")
    
    def is_time_restricted(self, app_config):
        """Check if app is time restricted"""
        if not app_config.get('time_restricted'):
            return False
        
        now = datetime.now().time()
        start_time = datetime.strptime(app_config.get('start_time', '00:00'), '%H:%M').time()
        end_time = datetime.strptime(app_config.get('end_time', '23:59'), '%H:%M').time()
        
        if start_time <= end_time:
            return start_time <= now <= end_time
        else:  # Crosses midnight
            return now >= start_time or now <= end_time
    
    def monitor_processes(self):
        """Monitor and block processes"""
        while self.monitoring:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'exe']):
                    try:
                        info = proc.info
                        exe_path = info.get('exe')
                        
                        if exe_path and exe_path in self.blocked_apps:
                            app_config = self.blocked_apps[exe_path]
                            
                            # Check if app should be blocked
                            should_block = app_config['blocked']
                            
                            if app_config.get('time_restricted'):
                                should_block = should_block and self.is_time_restricted(app_config)
                            
                            if should_block:
                                proc.terminate()
                                if self.show_notifications.get():
                                    self.show_notification(f"Blocked application: {app_config['name']}")
                                print(f"Blocked: {app_config['name']}")
                    
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"Error in monitoring: {e}")
                time.sleep(5)
    
    def start_monitoring(self):
        """Start process monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            self.monitor_thread.start()
            self.status_var.set("Ready - Monitoring: Active")
    
    def stop_monitoring(self):
        """Stop process monitoring"""
        self.monitoring = False
        self.status_var.set("Ready - Monitoring: Stopped")
    
    def show_notification(self, message):
        """Show system notification"""
        try:
            if NOTIFICATIONS_AVAILABLE and sys.platform == "win32":
                toaster = win10toast.ToastNotifier()
                toaster.show_toast("App Lock", message, duration=3)
            else:
                print(f"Notification: {message}")
        except Exception as e:
            print(f"Notification: {message} (Toast failed: {e})")
    
    def create_tray_image(self):
        """Create system tray icon"""
        if not TRAY_AVAILABLE:
            return None
        try:
            # Create a simple icon
            image = Image.new('RGB', (64, 64), color='red')
            draw = ImageDraw.Draw(image)
            draw.rectangle([16, 16, 48, 48], fill='white')
            draw.text((20, 25), "AL", fill='red')
            return image
        except Exception as e:
            print(f"Failed to create tray image: {e}")
            return None
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        if not TRAY_AVAILABLE:
            return
            
        try:
            image = self.create_tray_image()
            
            menu = pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Hide", self.hide_window),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Start Monitoring", self.start_monitoring),
                pystray.MenuItem("Stop Monitoring", self.stop_monitoring),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("AppLock", image, "App Lock Manager", menu)
            
            # Start tray in separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
        except Exception as e:
            print(f"Failed to setup system tray: {e}")
            self.tray_icon = None
    
    def show_window(self, icon=None, item=None):
        """Show main window with authentication check"""
        try:
            # Check if main window exists and is withdrawn
            if self.root.state() == 'withdrawn':
                # Create a simple authentication dialog
                auth_dialog = tk.Toplevel(self.root)
                auth_dialog.title("Authentication Required")
                auth_dialog.geometry("300x150")
                auth_dialog.configure(bg='#2c3e50')
                auth_dialog.resizable(False, False)
                auth_dialog.grab_set()
                
                # Center the dialog
                auth_dialog.update_idletasks()
                x = (auth_dialog.winfo_screenwidth() // 2) - (150)
                y = (auth_dialog.winfo_screenheight() // 2) - (75)
                auth_dialog.geometry(f'300x150+{x}+{y}')
                
                # Authentication form
                tk.Label(auth_dialog, text="Enter password to show window:", 
                        font=('Arial', 10, 'bold'), bg='#2c3e50', fg='white').pack(pady=10)
                
                # Create container for password entry
                entry_frame = tk.Frame(auth_dialog, bg='#2c3e50')
                entry_frame.pack(fill='x', padx=20, pady=5)
                
                entry_container = tk.Frame(entry_frame, bg='#3498db', relief='solid', bd=1)
                entry_container.pack(fill='x')
                
                password_var = tk.StringVar()
                password_entry = tk.Entry(entry_container, textvariable=password_var, 
                                         show='*', font=('Arial', 11),
                                         bg='white', fg='black',
                                         insertbackground='black',
                                         relief='flat', bd=0,
                                         highlightthickness=0)
                password_entry.pack(fill='x', padx=2, pady=2, ipady=6)
                
                def authenticate():
                    try:
                        if self.verify_password(password_var.get()):
                            auth_dialog.destroy()
                            self.root.deiconify()
                            self.root.lift()
                            self.root.focus_force()
                        else:
                            messagebox.showerror("Error", "Invalid password!", parent=auth_dialog)
                            password_var.set("")
                            password_entry.focus()
                    except Exception as e:
                        print(f"Authentication error: {e}")
                        auth_dialog.destroy()
                
                def cancel():
                    auth_dialog.destroy()
                
                # Buttons
                btn_frame = tk.Frame(auth_dialog, bg='#2c3e50')
                btn_frame.pack(pady=10)
                
                tk.Button(btn_frame, text="OK", command=authenticate,
                         bg='#27ae60', fg='white', relief='flat').pack(side='left', padx=5)
                tk.Button(btn_frame, text="Cancel", command=cancel,
                         bg='#e74c3c', fg='white', relief='flat').pack(side='left', padx=5)
                
                # Bind Enter key and focus
                password_entry.bind('<Return>', lambda e: authenticate())
                password_entry.focus_set()
            else:
                # Window is already visible, just bring it to front
                self.root.deiconify()
                self.root.lift()
                self.root.focus_force()
        except Exception as e:
            print(f"Error showing window: {e}")
            # Fallback: just show the window without authentication
            try:
                self.root.deiconify()
                self.root.lift()
            except:
                pass
    
    def hide_window(self, icon=None, item=None):
        """Hide main window"""
        self.root.withdraw()
    
    def on_closing(self):
        """Handle window close event"""
        try:
            if hasattr(self, 'minimize_to_tray') and self.minimize_to_tray.get() and TRAY_AVAILABLE:
                self.hide_window()
            else:
                self.quit_app()
        except Exception as e:
            print(f"Error in on_closing: {e}")
            self.quit_app()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        try:
            self.monitoring = False
            if hasattr(self, 'tray_icon') and self.tray_icon:
                try:
                    self.tray_icon.stop()
                except:
                    pass
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"Error during quit: {e}")
            try:
                self.root.destroy()
            except:
                pass
            sys.exit(0)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    # Check if running as administrator (recommended)
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("Warning: Not running as administrator. Some features may not work properly.")
    except:
        pass
    
    # Show login window first
    login_window = LoginWindow()
    authenticated = login_window.run()
    
    # Only proceed if authentication was successful
    if authenticated:
        print("Authentication successful. Starting main application...")
        app = AppLockManager()
        app.run()
    else:
        print("Authentication failed or cancelled. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()