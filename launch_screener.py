import subprocess
import os

# Path to your Python script
script_path = "/Users/tengis/finance/screener.py"

def open_new_terminal():
    try:
        # Use AppleScript to open a new Terminal window and run the Python script
        subprocess.Popen([
            'osascript', '-e',
            f'tell application "Screener" to do script "cd {os.path.dirname(script_path)} && python3 {script_path}"'
        ])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    open_new_terminal()
