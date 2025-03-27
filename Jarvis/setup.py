import os
import sys
import subprocess

def setup_environment():
    """Setup the project environment"""
    print("Setting up Jarvis AI Assistant...")
    
    # Install requirements
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Create necessary directories
    directories = [
        'Data',
        'Frontend/Files',
        'Frontend/Graphics/cache'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create .env if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env.template', 'r') as template, open('.env', 'w') as env:
            env.write(template.read())
        print("Created .env file from template. Please edit it with your API keys.")

if __name__ == "__main__":
    setup_environment() 