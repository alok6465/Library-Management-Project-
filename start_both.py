import subprocess
import sys
import os
import time

def start_applications():
    print("Starting Library Management System...")
    print("Main System: http://localhost:5000")
    print("File Viewer: http://localhost:5001")
    print("=" * 50)
    
    try:
        # Start main library system
        main_process = subprocess.Popen([
            sys.executable, "run.py"
        ], cwd=os.getcwd())
        
        # Start file viewer
        file_viewer_process = subprocess.Popen([
            sys.executable, "app_simple.py"
        ], cwd=os.path.join(os.getcwd(), "file_viewer"))
        
        print("Both applications started successfully!")
        print("Open your browser and visit:")
        print("   Main System: http://localhost:5000")
        print("   File Viewer: http://localhost:5001")
        print("\nPress Ctrl+C to stop both applications")
        
        # Wait for processes
        try:
            main_process.wait()
            file_viewer_process.wait()
        except KeyboardInterrupt:
            print("\nStopping applications...")
            main_process.terminate()
            file_viewer_process.terminate()
            print("Applications stopped successfully!")
            
    except Exception as e:
        print(f"Error starting applications: {e}")

if __name__ == "__main__":
    start_applications()