#!/usr/bin/env python3
"""Window monitoring module for cat-window-watcher."""

import os
import platform
import subprocess


class WindowMonitor:
    """Monitor active window titles across different platforms."""

    @staticmethod
    def is_screensaver_active(debug=False):
        """Check if screensaver is currently active.

        Args:
            debug: If True, print debug information about screensaver detection

        Returns:
            bool: True if screensaver is active, False otherwise
        """
        system = platform.system()

        try:
            if system == "Linux":
                result = WindowMonitor._is_screensaver_active_linux()
            elif system == "Darwin":  # macOS
                result = WindowMonitor._is_screensaver_active_macos()
            elif system == "Windows":
                result = WindowMonitor._is_screensaver_active_windows(debug=debug)
            else:
                result = False

            if debug:
                print(f"[DEBUG] Screensaver detection result: {result}")

            return result
        except Exception as e:
            if debug:
                print(f"[DEBUG] Exception during screensaver detection: {e}")
            print(f"Warning: Failed to check screensaver status: {e}")
            return False

    @staticmethod
    def get_active_window_title():
        """Get the title of the currently active window.

        Returns:
            str: Title of active window, or empty string if unable to get

        Raises:
            NotImplementedError: If platform is not supported
        """
        system = platform.system()

        try:
            if system == "Linux":
                return WindowMonitor._get_active_window_linux()
            elif system == "Darwin":  # macOS
                return WindowMonitor._get_active_window_macos()
            elif system == "Windows":
                return WindowMonitor._get_active_window_windows()
            else:
                raise NotImplementedError(f"Platform '{system}' is not supported")
        except Exception as e:
            print(f"Warning: Failed to get active window title: {e}")
            return ""

    @staticmethod
    def _get_active_window_linux():
        """Get active window title on Linux using xdotool.

        Returns:
            str: Window title

        Raises:
            OSError: If xdotool is not available
        """
        try:
            # Try xdotool first
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True,
                text=True,
                check=True,
                timeout=1,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # Fallback to xprop
            try:
                result = subprocess.run(
                    ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=1,
                )
                window_id = result.stdout.split()[-1]
                result = subprocess.run(
                    ["xprop", "-id", window_id, "WM_NAME"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=1,
                )
                # Extract title from output like: WM_NAME(STRING) = "Title"
                if "=" in result.stdout:
                    title = result.stdout.split("=", 1)[1].strip().strip('"')
                    return title
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_active_window_macos():
        """Get active window title on macOS using AppleScript.

        Returns:
            str: Window title
        """
        try:
            script = 'tell application "System Events" to get name of first application process whose frontmost is true'
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                check=True,
                timeout=1,
            )
            return result.stdout.strip()
        except Exception:
            return ""

    @staticmethod
    def _get_active_window_windows():
        """Get active window title on Windows using win32gui.

        Returns:
            str: Window title
        """
        try:
            import win32gui

            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except ImportError:
            # Fallback: try using PowerShell
            try:
                script = 'Add-Type @"\nusing System;\nusing System.Runtime.InteropServices;\npublic class Window {\n[DllImport("user32.dll")]\npublic static extern IntPtr GetForegroundWindow();\n[DllImport("user32.dll")]\npublic static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);\n}\n"@\n$h = [Window]::GetForegroundWindow()\n$s = New-Object System.Text.StringBuilder 256\n[Window]::GetWindowText($h, $s, 256)\n$s.ToString()'
                result = subprocess.run(
                    ["powershell", "-Command", script],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=2,
                )
                return result.stdout.strip()
            except Exception:
                return ""
        except Exception:
            return ""

    @staticmethod
    def _is_screensaver_active_linux():
        """Check if screensaver is active on Linux.

        Returns:
            bool: True if screensaver is active, False otherwise
        """
        # Try gnome-screensaver first (GNOME desktop environment)
        try:
            result = subprocess.run(
                ["gnome-screensaver-command", "-q"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            # Output contains "The screensaver is active" when active
            if result.returncode == 0 and "is active" in result.stdout.lower():
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # gnome-screensaver-command not available or too slow; try next method
            pass

        # Try xscreensaver (older or alternative desktop environments)
        try:
            result = subprocess.run(
                ["xscreensaver-command", "-time"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            # Output contains "screen blanked" or "screen locked" when active
            if result.returncode == 0 and ("blanked" in result.stdout.lower() or "locked" in result.stdout.lower()):
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # xscreensaver-command not available or too slow; try next method
            pass

        # Try checking for DPMS (Display Power Management Signaling) state
        # Note: DPMS detects display power-saving state, not strictly screensaver.
        # This catches cases where the display is in standby/suspend/off mode,
        # which often indicates the user is away (idle detection).
        try:
            result = subprocess.run(
                ["xset", "q"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            if result.returncode == 0:
                # Check if display is in standby/suspend/off state
                # DPMS output looks like: "  Monitor is On" or "  Monitor is Standby"
                dpms_section = False
                for line in result.stdout.split("\n"):
                    if "DPMS" in line:
                        dpms_section = True
                    if dpms_section and "Monitor is" in line:
                        # Check if monitor is in power-saving state
                        if any(state in line for state in ["Standby", "Suspend", "Off"]):
                            return True
                        break  # Stop after finding Monitor status
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # xset not available or too slow; no more methods to try
            pass

        return False

    @staticmethod
    def _is_screensaver_active_macos():
        """Check if screensaver is active on macOS.

        Returns:
            bool: True if screensaver is active, False otherwise
        """
        try:
            # Check if ScreenSaverEngine process is running
            script = 'tell application "System Events" to get name of every process'
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=1,
            )
            if result.returncode == 0 and "ScreenSaverEngine" in result.stdout:
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # osascript not available or too slow; screensaver not detected
            pass

        return False

    @staticmethod
    def _get_windows_process_info(hwnd, win32process):
        """Get process information for a Windows window handle.

        Args:
            hwnd: Window handle
            win32process: win32process module

        Returns:
            tuple: (process_id, process_executable_path) or (None, None) if unavailable
        """
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # Try using psutil if available
            try:
                import psutil

                process = psutil.Process(pid)
                process_exe = process.exe()
                return (pid, process_exe)
            except ImportError:
                # psutil not available
                return (pid, None)
            except Exception:
                # Could not get process details
                return (pid, None)
        except Exception:
            return (None, None)

    @staticmethod
    def _is_screensaver_active_windows(debug=False):
        """Check if screensaver is active on Windows.

        Args:
            debug: If True, print debug information

        Returns:
            bool: True if screensaver is active, False otherwise
        """
        try:
            import win32gui
            import win32process

            # Get the foreground window class name
            hwnd = win32gui.GetForegroundWindow()
            class_name = win32gui.GetClassName(hwnd)

            # Get process information
            pid, process_exe = WindowMonitor._get_windows_process_info(hwnd, win32process)

            if debug:
                window_title = win32gui.GetWindowText(hwnd)
                print("[DEBUG] Windows screensaver check (win32gui):")
                print(f"[DEBUG]   - Window handle: {hwnd}")
                print(f"[DEBUG]   - Window class name: '{class_name}'")
                print(f"[DEBUG]   - Window title: '{window_title}'")

                if pid is not None:
                    print(f"[DEBUG]   - Process ID: {pid}")

                    if process_exe is not None:
                        process_name = os.path.basename(process_exe)
                        print(f"[DEBUG]   - Process name: {process_name}")
                        print(f"[DEBUG]   - Process executable: {process_exe}")

                        # Check if it's a screensaver executable (.scr file)
                        if process_exe.lower().endswith(".scr"):
                            print("[DEBUG]   - Process is a .scr file (screensaver executable)")
                            # Specifically identify scrnsave.scr (Blank screensaver)
                            if "scrnsave.scr" in process_exe.lower():
                                print("[DEBUG]   - Detected: Blank screensaver (scrnsave.scr)")
                    else:
                        print("[DEBUG]   - psutil not available for detailed process info")
                else:
                    print("[DEBUG]   - Could not get process information")

            # Method 1: Check if window class name contains "screensaver"
            # Windows screensaver class name is typically "WindowsScreenSaverClass"
            if "screensaver" in class_name.lower():
                if debug:
                    print("[DEBUG]   - Screensaver detected via class name")
                return True

            # Method 2: Check if the foreground process is a screensaver executable (.scr)
            # This catches all screensavers including scrnsave.scr (Blank screensaver)
            if process_exe is not None and process_exe.lower().endswith(".scr"):
                if debug:
                    print("[DEBUG]   - Screensaver detected via .scr process")
                return True
        except ImportError:
            if debug:
                print("[DEBUG] Windows screensaver check: win32gui not available, trying PowerShell")
            # Fallback: try using PowerShell
            try:
                # PowerShell script to check if screensaver is running using SystemParametersInfo API
                script = (
                    "$signature = @'\n"
                    '[DllImport("user32.dll")]\n'
                    "public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, ref uint pvParam, uint fWinIni);\n"
                    "'@\n"
                    "$type = Add-Type -MemberDefinition $signature -Name Win32Utils -Namespace ScreenSaver -PassThru\n"
                    "$running = 0\n"
                    "$type::SystemParametersInfo(0x0072, 0, [ref]$running, 0)\n"
                    "$running"
                )
                result = subprocess.run(
                    ["powershell", "-Command", script],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )

                if debug:
                    print(
                        f"[DEBUG] PowerShell result: returncode={result.returncode}, stdout='{result.stdout.strip()}'"
                    )

                if result.returncode == 0 and result.stdout.strip() == "1":
                    if debug:
                        print("[DEBUG]   - Screensaver detected via PowerShell")
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                if debug:
                    print(f"[DEBUG] PowerShell check failed: {e}")
                # PowerShell is unavailable or too slow; fall back to default False
                pass
        except Exception as e:
            if debug:
                print(f"[DEBUG] Unexpected error in Windows screensaver detection: {e}")
            # Any other unexpected error should not crash the application
            pass

        return False
