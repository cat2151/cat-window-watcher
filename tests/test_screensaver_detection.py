#!/usr/bin/env python3
"""Tests for screensaver detection functionality."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

try:
    from src.score_tracker import ScoreTracker
    from src.window_monitor import WindowMonitor
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from score_tracker import ScoreTracker
    from window_monitor import WindowMonitor


class TestScreensaverDetection(unittest.TestCase):
    """Test cases for screensaver detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
        ]
        self.tracker = ScoreTracker(self.patterns, default_score=-1)

    def test_screensaver_active_no_score_change(self):
        """Test that score doesn't change when screensaver is active."""
        # Update with screensaver inactive first
        self.tracker.update("GitHub - Pull Requests", is_screensaver=False)
        self.assertEqual(self.tracker.get_score(), 10)

        # Update with screensaver active - score should not change
        score_changed, matched = self.tracker.update("", is_screensaver=True)
        self.assertFalse(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(matched.get("description"), "スクリーンセーバー")
        self.assertEqual(matched.get("score"), 0)
        self.assertEqual(self.tracker.get_score(), 10)  # Score unchanged

    def test_screensaver_description(self):
        """Test that screensaver shows correct description."""
        score_changed, matched = self.tracker.update("", is_screensaver=True)
        self.assertIsNotNone(matched)
        self.assertEqual(matched.get("description"), "スクリーンセーバー")
        self.assertEqual(matched.get("score"), 0)

    def test_screensaver_prevents_default_score(self):
        """Test that default score is not applied during screensaver."""
        # With a window that doesn't match any pattern, default score would be applied
        score_changed, matched = self.tracker.update("Unknown Window", is_screensaver=False)
        self.assertTrue(score_changed)
        self.assertEqual(self.tracker.get_score(), -1)  # default_score applied

        # Reset score
        self.tracker.reset_score()

        # But with screensaver active, no score change
        score_changed, matched = self.tracker.update("Unknown Window", is_screensaver=True)
        self.assertFalse(score_changed)
        self.assertEqual(self.tracker.get_score(), 0)  # No change

    def test_multiple_screensaver_updates(self):
        """Test multiple updates while screensaver is active."""
        # Set initial score
        self.tracker.update("GitHub", is_screensaver=False)
        initial_score = self.tracker.get_score()
        self.assertEqual(initial_score, 10)

        # Multiple screensaver updates should not change score
        for _ in range(5):
            score_changed, matched = self.tracker.update("", is_screensaver=True)
            self.assertFalse(score_changed)
            self.assertEqual(self.tracker.get_score(), initial_score)

    def test_screensaver_to_normal_transition(self):
        """Test transition from screensaver to normal window."""
        # Start with screensaver
        self.tracker.update("", is_screensaver=True)
        self.assertEqual(self.tracker.get_score(), 0)

        # Transition to normal window
        score_changed, matched = self.tracker.update("GitHub", is_screensaver=False)
        self.assertTrue(score_changed)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_normal_to_screensaver_transition(self):
        """Test transition from normal window to screensaver."""
        # Start with normal window
        self.tracker.update("Twitter", is_screensaver=False)
        self.assertEqual(self.tracker.get_score(), -5)

        # Transition to screensaver - score should freeze
        score_changed, matched = self.tracker.update("", is_screensaver=True)
        self.assertFalse(score_changed)
        self.assertEqual(self.tracker.get_score(), -5)  # Score frozen

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_linux_screensaver_detection_gnome(self, mock_run, mock_system):
        """Test Linux screensaver detection with gnome-screensaver."""
        # Mock gnome-screensaver-command output when screensaver is active
        mock_run.return_value = MagicMock(returncode=0, stdout="The screensaver is active\n")

        result = WindowMonitor.is_screensaver_active()
        self.assertTrue(result)

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_linux_screensaver_detection_inactive(self, mock_run, mock_system):
        """Test Linux screensaver detection when inactive."""
        # Mock gnome-screensaver-command output when screensaver is inactive
        mock_run.return_value = MagicMock(returncode=0, stdout="The screensaver is inactive\n")

        result = WindowMonitor.is_screensaver_active()
        self.assertFalse(result)

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_linux_screensaver_detection_xscreensaver_active(self, mock_run, mock_system):
        """Test Linux screensaver detection with xscreensaver when active."""

        # Mock gnome-screensaver failing, then xscreensaver succeeding
        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "gnome-screensaver-command" in cmd:
                raise FileNotFoundError("gnome-screensaver not found")
            elif "xscreensaver-command" in cmd:
                return MagicMock(returncode=0, stdout="screen blanked since 10:30:00\n")
            return MagicMock(returncode=1, stdout="")

        mock_run.side_effect = side_effect

        result = WindowMonitor.is_screensaver_active()
        self.assertTrue(result)

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_linux_screensaver_detection_xscreensaver_locked(self, mock_run, mock_system):
        """Test Linux screensaver detection with xscreensaver when locked."""

        # Mock gnome-screensaver failing, then xscreensaver reporting locked state
        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "gnome-screensaver-command" in cmd:
                raise FileNotFoundError("gnome-screensaver not found")
            elif "xscreensaver-command" in cmd:
                return MagicMock(returncode=0, stdout="screen locked since 10:30:00\n")
            return MagicMock(returncode=1, stdout="")

        mock_run.side_effect = side_effect

        result = WindowMonitor.is_screensaver_active()
        self.assertTrue(result)

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_linux_screensaver_detection_dpms_standby(self, mock_run, mock_system):
        """Test Linux screensaver detection with DPMS in standby state."""

        # Mock gnome-screensaver and xscreensaver failing, then DPMS succeeding
        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "gnome-screensaver-command" in cmd:
                raise FileNotFoundError("gnome-screensaver not found")
            elif "xscreensaver-command" in cmd:
                raise FileNotFoundError("xscreensaver not found")
            elif "xset" in cmd:
                return MagicMock(
                    returncode=0,
                    stdout="DPMS is Enabled\n  Monitor is Standby\n",
                )
            return MagicMock(returncode=1, stdout="")

        mock_run.side_effect = side_effect

        result = WindowMonitor.is_screensaver_active()
        self.assertTrue(result)

    @patch("platform.system", return_value="Linux")
    @patch("subprocess.run")
    def test_linux_screensaver_detection_dpms_on(self, mock_run, mock_system):
        """Test Linux screensaver detection with DPMS monitor on (not in power-saving)."""

        # Mock all methods, DPMS reports monitor is on
        def side_effect(*args, **kwargs):
            cmd = args[0]
            if "gnome-screensaver-command" in cmd:
                raise FileNotFoundError("gnome-screensaver not found")
            elif "xscreensaver-command" in cmd:
                raise FileNotFoundError("xscreensaver not found")
            elif "xset" in cmd:
                return MagicMock(
                    returncode=0,
                    stdout="DPMS is Enabled\n  Monitor is On\n",
                )
            return MagicMock(returncode=1, stdout="")

        mock_run.side_effect = side_effect

        result = WindowMonitor.is_screensaver_active()
        self.assertFalse(result)

    @patch("platform.system", return_value="Darwin")
    @patch("subprocess.run")
    def test_macos_screensaver_detection_active(self, mock_run, mock_system):
        """Test macOS screensaver detection when active."""
        # Mock osascript output when ScreenSaverEngine is running
        mock_run.return_value = MagicMock(returncode=0, stdout="Finder, ScreenSaverEngine, Safari\n")

        result = WindowMonitor.is_screensaver_active()
        self.assertTrue(result)

    @patch("platform.system", return_value="Darwin")
    @patch("subprocess.run")
    def test_macos_screensaver_detection_inactive(self, mock_run, mock_system):
        """Test macOS screensaver detection when inactive."""
        # Mock osascript output when ScreenSaverEngine is not running
        mock_run.return_value = MagicMock(returncode=0, stdout="Finder, Safari, Terminal\n")

        result = WindowMonitor.is_screensaver_active()
        self.assertFalse(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_with_win32gui_active(self, mock_system):
        """Test Windows screensaver detection with win32gui when screensaver is active."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock()}):
            import sys

            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "WindowsScreenSaverClass"

            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            result = WindowMonitor.is_screensaver_active()
            self.assertTrue(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_with_win32gui_inactive(self, mock_system):
        """Test Windows screensaver detection with win32gui when screensaver is inactive."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock()}):
            import sys

            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "Chrome_WidgetWin_1"

            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            result = WindowMonitor.is_screensaver_active()
            self.assertFalse(result)

    @patch("platform.system", return_value="Windows")
    @patch("subprocess.run")
    def test_windows_screensaver_detection_powershell_active(self, mock_run, mock_system):
        """Test Windows screensaver detection with PowerShell when screensaver is active."""
        # win32gui not available, PowerShell returns 1 (screensaver active)
        mock_run.return_value = MagicMock(returncode=0, stdout="1\n")

        result = WindowMonitor.is_screensaver_active()
        self.assertTrue(result)

    @patch("platform.system", return_value="Windows")
    @patch("subprocess.run")
    def test_windows_screensaver_detection_powershell_inactive(self, mock_run, mock_system):
        """Test Windows screensaver detection with PowerShell when screensaver is inactive."""
        # win32gui not available, PowerShell returns 0 (screensaver inactive)
        mock_run.return_value = MagicMock(returncode=0, stdout="0\n")

        result = WindowMonitor.is_screensaver_active()
        self.assertFalse(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_fallback(self, mock_system):
        """Test Windows screensaver detection fallback when both methods fail."""
        # Since win32gui may not be available and PowerShell may fail,
        # we just test that it returns False and doesn't crash
        result = WindowMonitor.is_screensaver_active()
        self.assertIsInstance(result, bool)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_via_scr_process(self, mock_system):
        """Test Windows screensaver detection via .scr process name."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock(), "psutil": MagicMock()}):
            import sys

            # Setup win32gui mock
            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "SomeCustomClass"  # Not screensaver class
            mock_win32gui.GetWindowText.return_value = ""

            # Setup win32process mock
            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            # Setup psutil mock
            mock_psutil = sys.modules["psutil"]
            mock_process = MagicMock()
            mock_process.exe.return_value = r"C:\Windows\System32\Bubbles.scr"
            mock_psutil.Process.return_value = mock_process

            result = WindowMonitor.is_screensaver_active()
            self.assertTrue(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_non_scr_process(self, mock_system):
        """Test Windows screensaver detection with non-.scr process."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock(), "psutil": MagicMock()}):
            import sys

            # Setup win32gui mock
            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "Chrome_WidgetWin_1"
            mock_win32gui.GetWindowText.return_value = "Google Chrome"

            # Setup win32process mock
            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            # Setup psutil mock
            mock_psutil = sys.modules["psutil"]
            mock_process = MagicMock()
            mock_process.exe.return_value = r"C:\Program Files\Google\Chrome\chrome.exe"
            mock_psutil.Process.return_value = mock_process

            result = WindowMonitor.is_screensaver_active()
            self.assertFalse(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_without_psutil(self, mock_system):
        """Test Windows screensaver detection when psutil is not available."""
        # Mock only win32gui and win32process, psutil not available
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock()}):
            import sys

            # Setup win32gui mock
            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "SomeCustomClass"
            mock_win32gui.GetWindowText.return_value = ""

            # Setup win32process mock
            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            # No psutil available - should not crash
            result = WindowMonitor.is_screensaver_active()
            self.assertIsInstance(result, bool)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_scr_with_class_name(self, mock_system):
        """Test Windows screensaver detection with both class name and .scr process."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock(), "psutil": MagicMock()}):
            import sys

            # Setup win32gui mock - with screensaver class name
            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "WindowsScreenSaverClass"
            mock_win32gui.GetWindowText.return_value = ""

            # Setup win32process mock
            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            # Setup psutil mock - also .scr file
            mock_psutil = sys.modules["psutil"]
            mock_process = MagicMock()
            mock_process.exe.return_value = r"C:\Windows\System32\Mystify.scr"
            mock_psutil.Process.return_value = mock_process

            # Should detect via class name (first method)
            result = WindowMonitor.is_screensaver_active()
            self.assertTrue(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_scrnsave_scr(self, mock_system):
        """Test Windows screensaver detection for scrnsave.scr (Blank screensaver)."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock(), "psutil": MagicMock()}):
            import sys

            # Setup win32gui mock - not standard screensaver class
            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "SomeOtherClass"
            mock_win32gui.GetWindowText.return_value = ""

            # Setup win32process mock
            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            # Setup psutil mock - scrnsave.scr (Blank screensaver)
            mock_psutil = sys.modules["psutil"]
            mock_process = MagicMock()
            mock_process.exe.return_value = r"C:\Windows\System32\scrnsave.scr"
            mock_psutil.Process.return_value = mock_process

            # Should detect via scrnsave.scr specific check
            result = WindowMonitor.is_screensaver_active()
            self.assertTrue(result)

    @patch("platform.system", return_value="Windows")
    def test_windows_screensaver_detection_scrnsave_scr_with_class_name(self, mock_system):
        """Test Windows screensaver detection for scrnsave.scr with standard class name."""
        # Mock win32gui and win32process modules
        with patch.dict("sys.modules", {"win32gui": MagicMock(), "win32process": MagicMock(), "psutil": MagicMock()}):
            import sys

            # Setup win32gui mock - with standard screensaver class
            mock_win32gui = sys.modules["win32gui"]
            mock_win32gui.GetForegroundWindow.return_value = 12345
            mock_win32gui.GetClassName.return_value = "WindowsScreenSaverClass"
            mock_win32gui.GetWindowText.return_value = ""

            # Setup win32process mock
            mock_win32process = sys.modules["win32process"]
            mock_win32process.GetWindowThreadProcessId.return_value = (1, 9999)

            # Setup psutil mock - scrnsave.scr (Blank screensaver)
            mock_psutil = sys.modules["psutil"]
            mock_process = MagicMock()
            mock_process.exe.return_value = r"C:\Windows\System32\scrnsave.scr"
            mock_psutil.Process.return_value = mock_process

            # Should detect via class name (first method)
            result = WindowMonitor.is_screensaver_active()
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
