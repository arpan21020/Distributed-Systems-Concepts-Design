import subprocess

# Define the command to run the Python file in a new terminal
def run_python_file(file_name):
    command = f"start cmd /k python {file_name}"
    subprocess.run(command, shell=True)



run_python_file('message_app_server.py')
run_python_file('group_server.py localhost 5556 localhost 5555')
run_python_file('group_server.py localhost 5557 localhost 5555')
run_python_file('client_server.py localhost')


