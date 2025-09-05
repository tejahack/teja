# Windows App Lock Manager

A comprehensive Windows application that allows you to block/lock access to specific applications with time-based restrictions and password protection.

## Features

### 🔒 Application Blocking
- Block any Windows application by selecting its executable file
- Real-time process monitoring and automatic termination of blocked apps
- Support for custom display names for better organization

### ⏰ Time-Based Restrictions
- Set specific time windows when applications should be blocked
- Perfect for parental controls or productivity management
- Supports time ranges that cross midnight

### 🔐 Security Features
- **Login Authentication**: Password required to start the application
- **System Tray Protection**: Password required to show window from system tray
- **Failed Attempt Protection**: Temporary lockout after 3 failed login attempts (30 seconds)
- **Secure Password Storage**: SHA-256 password hashing
- **Settings Protection**: Prevent unauthorized changes to blocked applications list

### 🖥️ User Interface
- Modern, intuitive GUI built with tkinter
- Tabbed interface for easy navigation
- Real-time process viewer with filtering capabilities
- System tray integration for background operation

### 📊 Process Management
- View all running processes with CPU and memory usage
- Kill processes directly from the application
- Search and filter processes by name

### ⚙️ Configuration Management
- Export/import configuration settings
- Persistent settings storage in JSON format
- Auto-save functionality

## Installation

### Prerequisites
- Windows 10/11
- Python 3.7 or higher
- Administrator privileges (recommended for full functionality)

### Setup Instructions

1. **Clone or download the application files**
   ```bash
   # If using git
   git clone <repository-url>
   cd windows_app_lock
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### Running as Administrator
For optimal functionality, especially when blocking system applications, run the application as administrator:

1. Right-click on Command Prompt
2. Select "Run as administrator"
3. Navigate to the application directory
4. Run `python main.py`

## Usage Guide

### First Time Setup

1. **Launch the application**
   - You'll be prompted with a login screen
   - Enter the default password: `admin123`
   - **IMPORTANT**: Change this password immediately in the Settings tab after login

2. **Login Security Features**
   - Maximum 3 login attempts before 30-second lockout
   - Password is required every time you start the application
   - System tray access also requires password authentication

3. **Add Applications to Block**
   - Go to the "Blocked Applications" tab
   - Click "Browse" to select an application executable (.exe file)
   - Enter a display name for the application
   - Optionally set time restrictions
   - Click "Add Application"

3. **Configure Time Restrictions (Optional)**
   - Check "Time Restricted" when adding an application
   - Set start and end times in HH:MM format (24-hour)
   - The application will only be blocked during specified hours

### Managing Blocked Applications

- **View blocked apps**: All blocked applications are listed in the main tab
- **Remove apps**: Select an application and click "Remove Selected"
- **Monitor status**: The status column shows if blocking is currently active

### Process Management

- **View processes**: Switch to "Running Processes" tab
- **Filter processes**: Use the filter box to search for specific processes
- **Kill processes**: Select a process and click "Kill Selected Process"
- **Refresh list**: Click "Refresh Processes" to update the list

### Settings Configuration

#### Password Settings
- Change the default password for security
- Requires current password verification
- Minimum 6 characters required

#### Monitoring Options
- **Auto-start monitoring**: Begin monitoring when application launches
- **Minimize to tray**: Hide to system tray instead of closing
- **Show notifications**: Display alerts when blocking applications

#### Configuration Management
- **Export Config**: Save current settings to a JSON file
- **Import Config**: Load settings from a previously saved file

## System Tray Integration

When minimized to the system tray, you can:
- Show/hide the main window
- Start/stop monitoring
- Exit the application

Right-click the tray icon to access these options.

## Technical Details

### How It Works
1. **Process Monitoring**: Continuously scans running processes every 2 seconds
2. **Path Matching**: Compares process executable paths with blocked applications list
3. **Time Validation**: Checks current time against configured restrictions
4. **Process Termination**: Terminates blocked processes using `psutil.Process.terminate()`

### Security Features
- Passwords are hashed using SHA-256
- Configuration files are stored locally in JSON format
- No network communication or data transmission

### Performance
- Lightweight process monitoring (2-second intervals)
- Minimal CPU and memory usage
- Efficient process filtering and searching

## Troubleshooting

### Common Issues

1. **"Access Denied" when killing processes**
   - Run the application as administrator
   - Some system processes cannot be terminated

2. **Application not blocking properly**
   - Ensure the correct executable path is configured
   - Check if time restrictions are properly set
   - Verify monitoring is active (status bar)

3. **System tray icon not appearing**
   - Check if system tray notifications are enabled
   - Restart the application
   - Some antivirus software may block tray integration

4. **Configuration not saving**
   - Check file permissions in the application directory
   - Ensure the application has write access
   - Run as administrator if needed

### Performance Optimization

- Close unused tabs to reduce memory usage
- Limit the number of blocked applications for faster monitoring
- Use specific time restrictions to reduce unnecessary blocking

## Security Considerations

### Important Notes
- **Password Protection**: The application requires authentication on every startup
- **System Tray Security**: Accessing the app from system tray also requires password
- **Failed Attempt Protection**: After 3 failed login attempts, the app locks for 30 seconds
- **Process Termination**: This application can terminate any running process
- **Administrator Privileges**: Use administrator privileges responsibly
- **Password Security**: Keep your password secure and change it regularly
- **Configuration Security**: Be cautious when importing configuration files from untrusted sources

### Security Features
- **SHA-256 Password Hashing**: Passwords are securely hashed and never stored in plain text
- **Login Attempt Monitoring**: Failed attempts are tracked and cause temporary lockouts
- **Session Protection**: No persistent login sessions - authentication required each time

### Limitations
- Cannot block applications that restart automatically
- Some system-critical processes may not be terminable
- Antivirus software may flag process termination activities
- Login lockout can be bypassed by restarting the application (by design for recovery)

## File Structure

```
windows_app_lock/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
└── app_lock_config.json   # Configuration file (created automatically)
```

## Contributing

This application is designed to be easily extensible. Key areas for enhancement:
- Additional notification methods
- More sophisticated time restrictions
- Application usage statistics
- Remote configuration management

## License

This project is provided as-is for educational and personal use. Use responsibly and in accordance with local laws and regulations.

## Support

For issues, questions, or feature requests, please refer to the troubleshooting section or create an issue in the project repository.

---

**⚠️ Important**: This application can terminate running processes and should be used responsibly. Always test with non-critical applications first.