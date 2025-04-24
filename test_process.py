import os
import time
import ctypes

# Define the test variable
my_var = ctypes.c_int(1337)

# Print necessary details for debugger
print("\n=== Test Process Running ===")
print(f"▶ PID: {os.getpid()}")
print(f"▶ Address of my_var: {hex(ctypes.addressof(my_var))}")
print(f"▶ Initial value of my_var: {my_var.value}")
print("============================\n")

# Helper functions
def show_value():
    print(f"[my_var value] = {my_var.value}")

def modify_value():
    my_var.value += 1
    print(f"[my_var updated] = {my_var.value}")

# Keep the process alive and interactive
while True:
    show_value()
    time.sleep(3)
    modify_value()
    time.sleep(2)
