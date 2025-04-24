import win32api
import win32con
import win32process
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
                win32api.SuspendThread(h_thread)
                win32api.CloseHandle(h_thread)
        print(f"[+] Suspended {len(thread_ids)} threads")

    def resume_process(self):
        print("[*] Resuming process...")
        thread_ids = self._get_thread_ids()
        for tid in thread_ids:
            h_thread = win32api.OpenThread(win32con.THREAD_SUSPEND_RESUME, False, tid)
            if h_thread:
                win32api.ResumeThread(h_thread)
                win32api.CloseHandle(h_thread)
        print(f"[+] Resumed {len(thread_ids)} threads")

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
