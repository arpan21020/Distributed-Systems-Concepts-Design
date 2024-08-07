import subprocess
import sys


# Define the command to run in the new terminal window
def run_mac():
    command1 = "cd Desktop/DSCD/-Distributed-Systems-Concepts-Design/Assignment1/gRPC/Shopping_Platform/Code && python3 buyer.py 192.168.63.255 50054 35.193.207.146"
    command2 = "cd Desktop/DSCD/-Distributed-Systems-Concepts-Design/Assignment1/gRPC/Shopping_Platform/Code && python3 buyer.py 192.168.44.172 50056 35.193.207.146"

    command3 = "cd Desktop/DSCD/-Distributed-Systems-Concepts-Design/Assignment1/gRPC/Shopping_Platform/Code && python3 seller.py 192.168.63.255 50050 35.193.207.146"
    command4 = "cd Desktop/DSCD/-Distributed-Systems-Concepts-Design/Assignment1/gRPC/Shopping_Platform/Code && python3 seller.py 192.168.44.172 50048 35.193.207.146"

    # Open a new terminal window and run the command
    # subprocess.run(["osascript", "-e", f'tell app "Terminal" to do script "{command}"'])
    subprocess.run(
        ["osascript", "-e", f'tell app "Terminal" to do script "{command1}"']
    )
    subprocess.run(
        ["osascript", "-e", f'tell app "Terminal" to do script "{command3}"']
    )


def run_windows():
    command = "start cmd /k python ./buyer.py localhost 50054"
    command2 = "start cmd /k python ./buyer.py localhost 50056"
    subprocess.run(command, shell=True)
    subprocess.run(command2, shell=True)


if __name__ == "__main__":

    if sys.platform.startswith("darwin"):
        # macOS specific commands
        run_mac()
    elif sys.platform.startswith("win32"):
        # Windows specific commands
        run_windows()
    else:
        print("Unsupported operating system")
