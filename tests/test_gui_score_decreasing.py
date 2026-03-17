#!/usr/bin/env python3
"""Tests for GUI module - score decreasing topmost feature."""

import tempfile
import unittest
from pathlib import Path

try:
    from tests.gui_mock_base import Config, MockScoreDisplay, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import Config, MockScoreDisplay, ScoreTracker


class TestGuiScoreDecreasingTopmost(unittest.TestCase):
    """Test cases for GUI score decreasing topmost feature."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def _create_mock_gui(self, config_content):
        """Helper to create a GUI with mocked tkinter components."""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        patterns = config.get_window_patterns()
        score_tracker = ScoreTracker(
            patterns,
            config.get_default_score(),
            config.get_apply_default_score_mode(),
        )

        # Create GUI with MockScoreDisplay
        gui = MockScoreDisplay(score_tracker, config)

        return gui, gui.root

    def test_score_decreasing_topmost_feature_disabled(self):
        """Test that topmost is not updated when feature is disabled."""
        config_content = """
always_on_top_while_score_decreasing = false

[[window_patterns]]
regex = "test"
score = -5
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Simulate score decrease
        gui.score_tracker.update("test")

        # Call update
        result = gui._update_score_decreasing_topmost()

        # Should return False (no priority)
        self.assertFalse(result)

        # Should not call attributes
        mock_root.attributes.assert_not_called()

    def test_score_decreasing_topmost_score_decreasing(self):
        """Test that topmost is set to True when score is decreasing."""
        config_content = """
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        # Call update
        result = gui._update_score_decreasing_topmost()

        # Should return True (took priority)
        self.assertTrue(result)

        # Should set topmost to True
        mock_root.attributes.assert_called_once_with("-topmost", True)

    def test_score_decreasing_topmost_score_increasing(self):
        """Test that topmost is restored to configured value when score is not decreasing."""
        config_content = """
always_on_top = false
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)
        self.assertFalse(gui.score_tracker.is_score_decreasing())

        # Call update
        result = gui._update_score_decreasing_topmost()

        # Should return False (no priority)
        self.assertFalse(result)

        # Should restore topmost to False (always_on_top = false)
        mock_root.attributes.assert_called_once_with("-topmost", False)

    def test_score_decreasing_topmost_continuous_decrease(self):
        """Test that topmost stays True during continuous score decrease."""
        config_content = """
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First decrease
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), -5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

        # Reset mock
        mock_root.reset_mock()

        # Second decrease
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), -10)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

    def test_score_decreasing_topmost_stops_decreasing_restores_state(self):
        """Test that topmost is properly restored when score stops decreasing."""
        config_content = """
always_on_top = false
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score - should set topmost to True
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

        # Reset mock
        mock_root.reset_mock()

        # Now increase score again - should restore topmost to False (from always_on_top)
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 15)
        self.assertFalse(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertFalse(result)
        # Should restore topmost to False (always_on_top = false)
        mock_root.attributes.assert_called_with("-topmost", False)

    def test_score_decreasing_topmost_stops_with_always_on_top_true(self):
        """Test that topmost stays True when score stops decreasing and always_on_top is True."""
        config_content = """
always_on_top = true
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score - should set topmost to True
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

        # Reset mock
        mock_root.reset_mock()

        # Now score stays same - should maintain topmost to True (from always_on_top)
        # Use apply_default_score_mode = false to avoid changing score
        config_content_no_default = """
always_on_top = true
always_on_top_while_score_decreasing = true
apply_default_score_mode = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        # Recreate GUI with updated config
        self.config_path.write_text(config_content_no_default)
        gui.config.load_config(exit_on_error=False)

        # Update score tracker with new config
        gui.score_tracker.update_config(
            gui.config.get_window_patterns(),
            gui.config.get_default_score(),
            gui.config.get_apply_default_score_mode(),
        )

        gui.score_tracker.update("unknown")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertFalse(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertFalse(result)
        # Should keep topmost to True (always_on_top = true)
        mock_root.attributes.assert_called_with("-topmost", True)


if __name__ == "__main__":
    unittest.main()
