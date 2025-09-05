"""
Build script to create standalone executable using PyInstaller
Run this script to create a distributable .exe file
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single executable
        "--windowed",                   # No console window
        "--name", "WindowsAppLock",     # Executable name
        "--icon", "icon.ico",           # Icon file (if exists)
        "--add-data", "README.md;.",    # Include README
        "--hidden-import", "win10toast",
        "--hidden-import", "pystray",
        "--hidden-import", "PIL",
        "--hidden-import", "psutil",
        "main.py"
    ]
    
    # Remove icon parameter if icon file doesn't exist
    if not Path("icon.ico").exists():
        cmd.remove("--icon")
        cmd.remove("icon.ico")
    
    print("Building executable...")
    print("Command:", " ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build successful!")
        print("Executable created: dist/WindowsAppLock.exe")
        print("\nYou can now distribute the executable file.")
        
        # Create distribution folder with necessary files
        create_distribution()
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        print("Please check the error messages above.")

def create_distribution():
    """Create distribution folder with all necessary files"""
    dist_folder = Path("distribution")
    dist_folder.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path("dist/WindowsAppLock.exe")
    if exe_source.exists():
        import shutil
        shutil.copy2(exe_source, dist_folder / "WindowsAppLock.exe")
        
    # Copy README
    readme_source = Path("README.md")
    if readme_source.exists():
        import shutil
        shutil.copy2(readme_source, dist_folder / "README.md")
    
    # Create batch file for easy running
    batch_content = """@echo off
echo Starting Windows App Lock Manager...
echo.
echo IMPORTANT: For full functionality, run this as Administrator
echo Right-click this file and select "Run as administrator"
echo.
pause
WindowsAppLock.exe
"""
    
    with open(dist_folder / "Run_AppLock.bat", "w") as f:
        f.write(batch_content)
    
    print(f"\n📁 Distribution folder created: {dist_folder}")
    print("Contents:")
    for item in dist_folder.iterdir():
        print(f"  - {item.name}")

def create_icon():
    """Create a simple icon file if it doesn't exist"""
    if Path("icon.ico").exists():
        return
    
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        img = Image.new('RGBA', (64, 64), (255, 0, 0, 255))  # Red background
        draw = ImageDraw.Draw(img)
        
        # Draw a lock symbol
        draw.rectangle([20, 25, 44, 45], outline=(255, 255, 255), width=2)
        draw.rectangle([25, 30, 39, 45], fill=(255, 255, 255))
        draw.ellipse([25, 15, 39, 30], outline=(255, 255, 255), width=2)
        
        # Save as ICO
        img.save("icon.ico", format='ICO')
        print("Created icon.ico")
        
    except ImportError:
        print("Pillow not available, skipping icon creation")

def main():
    """Main build function"""
    print("Windows App Lock Manager - Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found in current directory")
        print("Please run this script from the application directory")
        return
    
    # Install dependencies
    print("1. Installing build dependencies...")
    install_pyinstaller()
    
    # Create icon
    print("\n2. Creating application icon...")
    create_icon()
    
    # Build executable
    print("\n3. Building executable...")
    build_executable()
    
    print("\n🎉 Build process completed!")
    print("\nNext steps:")
    print("1. Test the executable: dist/WindowsAppLock.exe")
    print("2. Distribute the files in the 'distribution' folder")
    print("3. Remind users to run as Administrator for full functionality")

if __name__ == "__main__":
    main()