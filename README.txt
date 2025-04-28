=====================================
Simple Windows Debugger in Python
SE 550 – Software Reverse Engineering
=====================================

This project implements a simple Windows debugger using Python.

The debugger can:
- Attach to a running process
- Suspend (halt) and resume process execution
- Read memory at specific addresses
- Inspect CPU thread registers
- Detach safely from the process

It demonstrates fundamental concepts in runtime software inspection and control.

-------------------------------------
 Project Structure:
-------------------------------------
/src/
    debugger.py         # Debugger core class
    main.py             # Command-line interface for debugger
    test_process.py     # Test process for debugging (Balanced CPU activity)
/docs/
    diagram.png         # (Optional) Visual diagram

README.txt
LICENSE (optional)

-------------------------------------
 How to Run:
-------------------------------------

1. Install Python 3.10+ (64-bit).

2. Create and activate a virtual environment:
   > cd src
   > py -3.10 -m venv .venv
   > .\.venv\Scripts\Activate.ps1
   > pip install pywin32

3. Open two terminals:

Terminal 1: (Run Test Process)
   > python test_process.py

Terminal 2: (Run Debugger)
   > python main.py

4. Attach to the printed PID and interact with the process.

-------------------------------------
Debugger Features:
-------------------------------------

 Attach to a running process using PID  
 Read memory from specific address  
 Suspend all threads (halt execution)  
 Resume all threads (continue execution)  
 Inspect CPU thread registers  
 Detach cleanly and exit

-------------------------------------
 Test Process Behavior:
-------------------------------------

- `test_process.py` automatically updates `my_var` (integer) rapidly.
- CPU is kept busy with heavy calculations (no idle sleeps).
- This improves chances of live register capture when inspecting.

Modes:
- Fast balanced updates (0.1 to 0.5 sec delay) are used to keep terminal readable.

-------------------------------------
 Important Notes:
-------------------------------------

- When inspecting registers (Option 5), registers may appear as `0x0`.
- This is because Python processes abstract low-level CPU register activity.
- In C/C++ programs, real live register values would appear.

 Your debugger still correctly captures thread context.

-------------------------------------
 Demo Flow:
-------------------------------------

1. Launch test_process.py (auto busy mode)
2. Note the PID and memory address
3. Launch main.py
4. Attach to PID
5. Choose from menu:
   - 1: Read memory
   - 2: Suspend process
   - 3: Resume process
   - 5: Inspect registers
   - 4: Detach and exit

-------------------------------------
 Safety:
-------------------------------------

- Detaching properly ensures no crash or corruption in the target process.
- Memory is read-only (no write operations are performed).

-------------------------------------
 Challenges and Improvements:
-------------------------------------

- High-level processes like Python abstract CPU registers.
- To improve register capture, attach to lower-level compiled programs (like C executables).

Future improvements could include:
- Setting breakpoints
- Stepping through instructions
- Handling multiple threads individually

-------------------------------------
 Author:
-------------------------------------
Yash Patel  
SE 550 – Spring 2025
St. Cloud State University
