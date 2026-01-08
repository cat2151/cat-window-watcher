#!/usr/bin/env python3
"""Window monitoring module for cat-window-watcher."""

import platform
import subprocess


class WindowMonitor:
    """Monitor active window titles across different platforms."""

    @staticmethod
    def is_screensaver_active():
        """Check if screensaver is currently active.

        Returns:
            bool: True if screensaver is active, False otherwise
        """
        system = platform.system()

        try:
            if system == "Linux":
                return WindowMonitor._is_screensaver_active_linux()
            elif system == "Darwin":  # macOS
                return WindowMonitor._is_screensaver_active_macos()
            elif system == "Windows":
                return WindowMonitor._is_screensaver_active_windows()
            else:
                return False
        except Exception as e:
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
            pass

        # Try checking for DPMS (Display Power Management Signaling) state
        try:
            result = subprocess.run(
                ["xset", "q"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            if result.returncode == 0:
                # Check if display is in standby/suspend/off state
                for line in result.stdout.split("\n"):
                    if "DPMS is Enabled" in line:
                        continue
                    if "Monitor is" in line and any(state in line for state in ["Standby", "Suspend", "Off"]):
                        return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
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
            pass

        return False

    @staticmethod
    def _is_screensaver_active_windows():
        """Check if screensaver is active on Windows.

        Returns:
            bool: True if screensaver is active, False otherwise
        """
        try:
            import win32gui

            # Get the foreground window class name
            hwnd = win32gui.GetForegroundWindow()
            class_name = win32gui.GetClassName(hwnd)

            # Windows screensaver class name is "WindowsScreenSaverClass"
            if "screensaver" in class_name.lower():
                return True
        except ImportError:
            # Fallback: try using PowerShell
            try:
                script = """
$signature = @'
[DllImport("user32.dll")]
public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, ref uint pvParam, uint fWinIni);
'@
$type = Add-Type -MemberDefinition $signature -Name Win32Utils -Namespace ScreenSaver -PassThru
$running = 0
$type::SystemParametersInfo(0x0072, 0, [ref]$running, 0)
$running
"""
                result = subprocess.run(
                    ["powershell", "-Command", script],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0 and result.stdout.strip() == "1":
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
        except Exception:
            pass

        return False
