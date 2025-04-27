import os
import time
import ctypes

# Define the test variable
my_var = ctypes.c_int(1337)

def show_intro():
    print("\n=== Test Process Running ===")
    print(f"▶ PID: {os.getpid()}")
    print(f"▶ Address of my_var (use this address in debugger): {hex(ctypes.addressof(my_var))}")
    print(f"▶ Initial value of my_var (4 bytes integer): {my_var.value}")
    print("============================\n")

def show_value():
    print(f"[+] Current value of my_var: {my_var.value}")

def modify_value_heavy():
    # Do heavy calculations
    for i in range(100000):
        my_var.value += i

def auto_busy_mode():
    while True:
        show_value()
        modify_value_heavy()  # Heavy calculations keep CPU busy
        time.sleep(0.5)       # Tiny sleep to slow flood

def main():
    show_intro()
    print("\nRunning in Busy Mode (CPU activity to fill registers).")
    auto_busy_mode()

if __name__ == "__main__":
    main()
