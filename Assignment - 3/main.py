import subprocess


# Define the command to run the Python file in a new terminal
def run_python_file(file_name):
    command = f"start cmd /k python3 {file_name}"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    m = int(input("Enter the number of mappers: "))
    r = int(input("Enter the number of reducers: "))
    k = int(input("Enter the number of centroids: "))
    run_python_file(f"master.py {m} {r} {k}")
    for id in range(m):
        run_python_file(f"mapper.py {50000+id}")
    for id in range(r):
        run_python_file(f"reducer.py {60000+id}")
