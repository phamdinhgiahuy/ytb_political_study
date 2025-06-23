#!/usr/bin/env python3
"""
Setup script for YouTube Political Study Scraper

This script helps users set up the environment and install dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def check_api_key():
    """Check if YouTube API key is set."""
    api_key = os.getenv("H_YOUTUBE_API_KEY")
    if api_key:
        print("✅ YouTube API key is set")
        return True
    else:
        print("❌ YouTube API key not found")
        print("\nTo set your API key, run:")
        print("export H_YOUTUBE_API_KEY=\"your_api_key_here\"")
        print("\nOr add it to your ~/.bashrc or ~/.zshrc file for persistence.")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ["data", "cache"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function."""
    print("YouTube Political Study Scraper - Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create directories
    create_directories()
    
    # Check API key
    api_key_set = check_api_key()
    
    print("\n" + "=" * 40)
    if api_key_set:
        print("✅ Setup completed successfully!")
        print("\nYou can now run the scraper with:")
        print("python youtube_scraper.py")
    else:
        print("⚠️  Setup completed, but you need to set your YouTube API key.")
        print("\nGet your API key from: https://console.cloud.google.com/")
        print("Then set it with: export H_YOUTUBE_API_KEY=\"your_key_here\"")

if __name__ == "__main__":
    main() 