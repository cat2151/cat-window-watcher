#!/usr/bin/env python3
"""Tests for GUI module - score color switching."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

try:
    from tests.gui_mock_base import Config, MockScoreDisplayWithColorTracking, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import Config, MockScoreDisplayWithColorTracking, ScoreTracker


class TestGuiScoreColors(unittest.TestCase):
    """Test cases for GUI score color switching."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_mock_gui(self, config_content):
        """Create a mock GUI with given configuration."""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))
        score_tracker = ScoreTracker(config.get_window_patterns(), config.get_default_score())
        window_monitor = MagicMock()
        gui = MockScoreDisplayWithColorTracking(score_tracker, window_monitor, config)
        return gui

    def test_score_color_increases_uses_up_color(self):
        """Test that score increase uses score_up_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Trigger score increase
        color = gui.update_display_color_logic("github.com")

        # Verify score_up_color is used
        self.assertEqual(color, "#00ff00")
        gui.score_label.config.assert_called_with(fg="#00ff00")

    def test_score_color_decreases_uses_down_color(self):
        """Test that score decrease uses score_down_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -15
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # First increase score
        gui.update_display_color_logic("github.com")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score
        color = gui.update_display_color_logic("twitter.com")

        # Verify score_down_color is used
        self.assertEqual(color, "#ff0000")
        self.assertEqual(gui.score_tracker.get_score(), -5)

    def test_score_color_stays_same_uses_up_color(self):
        """Test that no score change uses score_up_color."""
        config_content = """
score_up_color = "#ffffff"
score_down_color = "#ff0000"
default_score = 0
apply_default_score_mode = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # First increase score
        gui.update_display_color_logic("github.com")

        # Window that doesn't match any pattern (score stays same)
        color = gui.update_display_color_logic("random window")

        # Verify score_up_color is used (score didn't decrease)
        self.assertEqual(color, "#ffffff")

    def test_score_color_multiple_increases(self):
        """Test multiple consecutive score increases use score_up_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 5
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Multiple increases
        for _ in range(3):
            color = gui.update_display_color_logic("github.com")
            self.assertEqual(color, "#00ff00")

        # Final score should be 15
        self.assertEqual(gui.score_tracker.get_score(), 15)

    def test_score_color_multiple_decreases(self):
        """Test multiple consecutive score decreases use score_down_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Multiple decreases
        for _ in range(3):
            color = gui.update_display_color_logic("twitter.com")
            self.assertEqual(color, "#ff0000")

        # Final score should be -15
        self.assertEqual(gui.score_tracker.get_score(), -15)

    def test_score_color_alternating_changes(self):
        """Test alternating score increases and decreases use correct colors."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Increase
        color = gui.update_display_color_logic("github.com")
        self.assertEqual(color, "#00ff00")

        # Decrease
        color = gui.update_display_color_logic("twitter.com")
        self.assertEqual(color, "#ff0000")

        # Increase again
        color = gui.update_display_color_logic("github.com")
        self.assertEqual(color, "#00ff00")

        # Decrease again
        color = gui.update_display_color_logic("twitter.com")
        self.assertEqual(color, "#ff0000")

    def test_score_color_initial_state_uses_up_color(self):
        """Test that initial state (score 0) uses score_up_color."""
        config_content = """
score_up_color = "#ffffff"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui = self._create_mock_gui(config_content)

        # Initial score is 0, check that previous score is initialized correctly
        self.assertEqual(gui._previous_score, 0)

    def test_score_color_with_default_colors(self):
        """Test score color switching with default color values."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -15
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Increase - should use default #ffffff
        color = gui.update_display_color_logic("github.com")
        self.assertEqual(color, "#ffffff")

        # Decrease - should use default #ff0000
        color = gui.update_display_color_logic("twitter.com")
        self.assertEqual(color, "#ff0000")


if __name__ == "__main__":
    unittest.main()
