import win32api
import win32con
import ctypes
from ctypes import wintypes

PROCESS_ALL_ACCESS = 0x1F0FFF

class WindowsDebugger:
    def __init__(self):
        self.pid = None
        self.process_handle = None

    def attach(self, pid):
        self.pid = pid
        try:
            self.process_handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
            print(f"[+] Successfully attached to process {pid}")
        except Exception as e:
            print(f"[!] Failed to attach to process {pid}: {e}")

    def read_memory(self, address, size):
        data = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        address_ptr = ctypes.c_void_p(address)

        result = ctypes.windll.kernel32.ReadProcessMemory(
            self.process_handle.handle,
            address_ptr,
            data,
            size,
            ctypes.byref(bytes_read)
        )

        if result != 0:
            return data.raw
        else:
            print(f"[!] Failed to read memory at address {hex(address)}")
            return None

    def suspend_process(self):
        print("[*] Suspending process...")
        thread_ids = self._get_thread_ids()
        for tid in thread_ids:
            h_thread = win32api.OpenThread(win32con.THREAD_SUSPEND_RESUME, False, tid)
            if h_thread:
                ctypes.windll.kernel32.SuspendThread(h_thread.handle)
                win32api.CloseHandle(h_thread)
        print(f"[+] Suspended {len(thread_ids)} threads")

    def resume_process(self):
        print("[*] Resuming process...")
        thread_ids = self._get_thread_ids()
        for tid in thread_ids:
            h_thread = win32api.OpenThread(win32con.THREAD_SUSPEND_RESUME, False, tid)
            if h_thread:
                ctypes.windll.kernel32.ResumeThread(h_thread.handle)
                win32api.CloseHandle(h_thread)
        print(f"[+] Resumed {len(thread_ids)} threads")

    def inspect_registers(self):
        print("[*] Inspecting thread registers...")

        class CONTEXT(ctypes.Structure):
            _fields_ = [
                ("ContextFlags", wintypes.DWORD),
                ("Dr0", wintypes.DWORD),
                ("Dr1", wintypes.DWORD),
                ("Dr2", wintypes.DWORD),
                ("Dr3", wintypes.DWORD),
                ("Dr6", wintypes.DWORD),
                ("Dr7", wintypes.DWORD),
                ("FloatSave", ctypes.c_byte * 112),
                ("SegGs", wintypes.DWORD),
                ("SegFs", wintypes.DWORD),
                ("SegEs", wintypes.DWORD),
                ("SegDs", wintypes.DWORD),
                ("Edi", wintypes.DWORD),
                ("Esi", wintypes.DWORD),
                ("Ebx", wintypes.DWORD),
                ("Edx", wintypes.DWORD),
                ("Ecx", wintypes.DWORD),
                ("Eax", wintypes.DWORD),
                ("Ebp", wintypes.DWORD),
                ("Eip", wintypes.DWORD),
                ("SegCs", wintypes.DWORD),
                ("EFlags", wintypes.DWORD),
                ("Esp", wintypes.DWORD),
                ("SegSs", wintypes.DWORD),
            ]

        thread_ids = self._get_thread_ids()
        if not thread_ids:
            print("[!] No threads found.")
            return

        thread_handle = win32api.OpenThread(win32con.THREAD_GET_CONTEXT, False, thread_ids[0])

        context = CONTEXT()
        context.ContextFlags = 0x10007  # CONTEXT_CONTROL + CONTEXT_INTEGER

        result = ctypes.windll.kernel32.GetThreadContext(thread_handle.handle, ctypes.byref(context))

        if result:
            print(f"EAX = {hex(context.Eax)}")
            print(f"EBX = {hex(context.Ebx)}")
            print(f"ECX = {hex(context.Ecx)}")
            print(f"EDX = {hex(context.Edx)}")
            print(f"ESI = {hex(context.Esi)}")
            print(f"EDI = {hex(context.Edi)}")
            print(f"EBP = {hex(context.Ebp)}")
            print(f"ESP = {hex(context.Esp)}")
            print(f"EIP = {hex(context.Eip)}")
        else:
            print("[!] Failed to get thread context.")

        win32api.CloseHandle(thread_handle)

    def detach(self):
        if self.process_handle:
            win32api.CloseHandle(self.process_handle)
            print("[+] Detached from process.")

    def _get_thread_ids(self):
        class THREADENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ThreadID", wintypes.DWORD),
                ("th32OwnerProcessID", wintypes.DWORD),
                ("tpBasePri", wintypes.LONG),
                ("tpDeltaPri", wintypes.LONG),
                ("dwFlags", wintypes.DWORD),
            ]

        thread_ids = []
        CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
        Thread32First = ctypes.windll.kernel32.Thread32First
        Thread32Next = ctypes.windll.kernel32.Thread32Next
        CloseHandle = ctypes.windll.kernel32.CloseHandle

        snapshot = CreateToolhelp32Snapshot(0x00000004, 0)  # TH32CS_SNAPTHREAD = 0x4
        entry = THREADENTRY32()
        entry.dwSize = ctypes.sizeof(THREADENTRY32)

        success = Thread32First(snapshot, ctypes.byref(entry))
        while success:
            if entry.th32OwnerProcessID == self.pid:
                thread_ids.append(entry.th32ThreadID)
            success = Thread32Next(snapshot, ctypes.byref(entry))

        CloseHandle(snapshot)
        return thread_ids
