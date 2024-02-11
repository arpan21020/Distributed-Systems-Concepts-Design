import subprocess
import sys
# Define the command to run in the new terminal window
def run_mac():
    command = "python buyer.py localhost 50054"
    command2 = "python buyer.py localhost 50056"

    # Open a new terminal window and run the command
    subprocess.run(['osascript', '-e', f'tell app "Terminal" to do script "{command}"'])
    subprocess.run(['osascript', '-e', f'tell app "Terminal" to do script "{command2}"'])
def run_windows():
    command = "start cmd /k python ./buyer.py localhost 50054"
    command2 = "start cmd /k python ./buyer.py localhost 50056"
    subprocess.run(command, shell=True)
    subprocess.run(command2, shell=True)
    
if __name__ == "__main__":
    
    if sys.platform.startswith('darwin'):
        # macOS specific commands
        run_mac()
    elif sys.platform.startswith('win32'):
        # Windows specific commands
        run_windows()
    else:
        print("Unsupported operating system")