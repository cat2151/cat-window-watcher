#!/usr/bin/env python3
"""Window monitoring module for cat-window-watcher."""

import platform
import subprocess


class WindowMonitor:
    """Monitor active window titles across different platforms."""

    @staticmethod
    def is_screensaver_active(debug=False):
        """Check if screensaver is currently active.

        This uses a simplified approach: treats windows with empty titles as screensavers.
        This is more reliable than complex platform-specific detection methods.

        Args:
            debug: If True, print debug information about screensaver detection

        Returns:
            bool: True if screensaver is active (empty window title), False otherwise
        """
        # Get the current window title
        window_title = WindowMonitor.get_active_window_title()

        # Simplified approach: empty window title indicates screensaver
        result = window_title == ""

        if debug:
            print("[DEBUG] Screensaver detection (simplified):")
            print(f"[DEBUG]   - Window title: '{window_title}'")
            print(f"[DEBUG]   - Screensaver detected: {result}")

        return result

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
    def get_active_window_process_name():
        """Get the process name of the currently active window.

        Returns:
            str: Process name of active window, or empty string if unable to get

        Raises:
            NotImplementedError: If platform is not supported
        """
        system = platform.system()

        try:
            if system == "Linux":
                return WindowMonitor._get_active_window_process_name_linux()
            elif system == "Darwin":  # macOS
                return WindowMonitor._get_active_window_process_name_macos()
            elif system == "Windows":
                return WindowMonitor._get_active_window_process_name_windows()
            else:
                raise NotImplementedError(f"Platform '{system}' is not supported")
        except Exception as e:
            print(f"Warning: Failed to get active window process name: {e}")
            return ""

    @staticmethod
    def _get_active_window_process_name_linux():
        """Get active window process name on Linux.

        Returns:
            str: Process name
        """
        try:
            # Get window ID
            result = subprocess.run(
                ["xdotool", "getactivewindow"],
                capture_output=True,
                text=True,
                check=True,
                timeout=1,
            )
            window_id = result.stdout.strip()

            # Get PID from window ID
            result = subprocess.run(
                ["xdotool", "getwindowpid", window_id],
                capture_output=True,
                text=True,
                check=True,
                timeout=1,
            )
            pid = result.stdout.strip()

            # Get process name from PID
            result = subprocess.run(
                ["ps", "-p", pid, "-o", "comm="],
                capture_output=True,
                text=True,
                check=True,
                timeout=1,
            )
            return result.stdout.strip()
        except Exception:
            return ""

    @staticmethod
    def _get_active_window_process_name_macos():
        """Get active window process name on macOS using AppleScript.

        Returns:
            str: Process name
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
    def _get_active_window_process_name_windows():
        """Get active window process name on Windows.

        Returns:
            str: Process name
        """
        try:
            import psutil
            import win32gui
            import win32process

            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except ImportError:
            # Fallback: try using PowerShell
            # Simplified script that gets foreground window process in steps
            try:
                script = (
                    "Add-Type -AssemblyName System.Windows.Forms; "
                    "$hwnd = [System.Windows.Forms.Form]::ActiveForm; "
                    "if ($hwnd) { "
                    "    $pid = (Get-Process | Where-Object {$_.MainWindowHandle -eq $hwnd.Handle}).Id; "
                    "    (Get-Process -Id $pid).ProcessName "
                    "}"
                )
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
