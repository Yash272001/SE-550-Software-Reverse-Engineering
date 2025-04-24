from debugger import WindowsDebugger

def main():
    print("=== Python Debugger ===")
    try:
        pid = int(input("Enter PID to attach: "))
    except ValueError:
        print("[!] Invalid PID. Exiting.")
        return

    dbg = WindowsDebugger()
    dbg.attach(pid)

    while True:
        print("\nChoose an action:")
        print("1 - Read memory")
        print("2 - Suspend process (halt)")
        print("3 - Resume process")
        print("4 - Detach and exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            try:
                address_input = input("Enter memory address to read (in hex, e.g., 0x1234): ")
                address = int(address_input, 16)
                size = int(input("Enter number of bytes to read: "))
                data = dbg.read_memory(address, size)
                if data:
                    print(f"[+] Data at {hex(address)}: {data}")
            except Exception as e:
                print(f"[!] Error: {e}")

        elif choice == '2':
            dbg.suspend_process()

        elif choice == '3':
            dbg.resume_process()

        elif choice == '4':
            dbg.detach()
            break

        else:
            print("[!] Invalid option. Try again.")

if __name__ == "__main__":
    main()
