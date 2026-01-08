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
    def test_windows_screensaver_detection_fallback(self, mock_system):
        """Test Windows screensaver detection fallback when win32gui not available."""
        # Since win32gui may not be available in test environment, we just test that it doesn't crash
        result = WindowMonitor.is_screensaver_active()
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    unittest.main()
