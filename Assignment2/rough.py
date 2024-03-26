# import threading


# def hello():
#     print("Hello, World!")
#     # t = threading.Timer(2.0, hello)
#     # t.start()


# # create a timer that will run the hello function after 5 seconds


# t = threading.Timer(10, hello)
# t.start()  # after 30 seconds, "hello, World!" will be printed
# print("Hello, World!")
import sys
x = sys.argv[1:]
print(x)