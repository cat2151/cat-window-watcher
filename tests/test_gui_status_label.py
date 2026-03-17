#!/usr/bin/env python3
"""Tests for GUI module - status label display."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

try:
    from tests.gui_mock_base import MAX_WINDOW_TITLE_LENGTH, Config, MockScoreDisplayWithStatusLabel, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import MAX_WINDOW_TITLE_LENGTH, Config, MockScoreDisplayWithStatusLabel, ScoreTracker


class TestGuiStatusLabelDisplay(unittest.TestCase):
    """Test cases for GUI status label display with window titles."""

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
        gui = MockScoreDisplayWithStatusLabel(score_tracker, window_monitor, config)
        return gui

    def test_status_label_shows_matched_pattern(self):
        """Test that status label shows description and score for matched pattern."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with matched pattern
        gui.update_display_status_logic("GitHub - Profile")

        # Verify status label shows matched pattern info
        gui.status_label.config.assert_called_with(text="GitHub (+10)")

    def test_status_label_shows_window_title_with_default_score_negative(self):
        """Test that status label shows window title with default score when no match and default_score < 0."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with no match
        gui.update_display_status_logic("Random Window Title")

        # Verify status label shows window title with default score
        gui.status_label.config.assert_called_with(text="No match: Random Window Title (-1)")

    def test_status_label_shows_window_title_with_default_score_positive(self):
        """Test that status label shows window title with default score when no match and default_score > 0."""
        config_content = """
default_score = 5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with no match
        gui.update_display_status_logic("Some Application Window")

        # Verify status label shows window title with default score
        gui.status_label.config.assert_called_with(text="No match: Some Application Window (+5)")

    def test_status_label_shows_window_title_without_default_score_when_zero(self):
        """Test that status label shows only window title when no match and default_score = 0."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with no match
        gui.update_display_status_logic("Terminal - bash")

        # Verify status label shows only window title
        gui.status_label.config.assert_called_with(text="Terminal - bash")

    def test_status_label_truncates_long_window_title_with_default_score(self):
        """Test that long window titles are truncated when no match with default_score."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with long window title (over MAX_WINDOW_TITLE_LENGTH characters)
        long_title = "This is a very long window title that exceeds forty characters"
        gui.update_display_status_logic(long_title)

        # Verify status label shows truncated window title with ellipsis
        expected_text = f"No match: {long_title[:MAX_WINDOW_TITLE_LENGTH]}... (-1)"
        gui.status_label.config.assert_called_with(text=expected_text)

    def test_status_label_truncates_long_window_title_without_default_score(self):
        """Test that long window titles are truncated when no match without default_score."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with long window title (over MAX_WINDOW_TITLE_LENGTH characters)
        long_title = "This is a very long window title that exceeds forty characters"
        gui.update_display_status_logic(long_title)

        # Verify status label shows truncated window title with ellipsis
        expected_text = f"{long_title[:MAX_WINDOW_TITLE_LENGTH]}..."
        gui.status_label.config.assert_called_with(text=expected_text)

    def test_status_label_shows_watching_for_empty_window_title_without_default_score(self):
        """Test that status label shows 'Watching...' for empty window title without default_score."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with empty window title
        gui.update_display_status_logic("")

        # Verify status label shows "Watching..."
        gui.status_label.config.assert_called_with(text="Watching...")

    def test_status_label_shows_no_match_for_empty_window_title_with_default_score(self):
        """Test that status label shows 'No match (score)' for empty window title with default_score."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with empty window title
        gui.update_display_status_logic("")

        # Verify status label shows "No match (-1)"
        gui.status_label.config.assert_called_with(text="No match (-1)")

    def test_status_label_shows_window_title_with_special_characters(self):
        """Test that status label correctly shows window titles with special characters."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with special characters in window title
        special_title = "MyApp [Debug] - File.txt (Modified)"
        gui.update_display_status_logic(special_title)

        # Verify status label shows window title with special characters
        gui.status_label.config.assert_called_with(text=f"No match: {special_title} (-1)")

    def test_status_label_alternates_between_match_and_no_match(self):
        """Test that status label correctly alternates between matched and no-match states."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with matched pattern
        gui.update_display_status_logic("GitHub - Profile")
        gui.status_label.config.assert_called_with(text="GitHub (+10)")

        # Test with no match
        gui.update_display_status_logic("Random Window")
        gui.status_label.config.assert_called_with(text="No match: Random Window (-1)")

        # Test with matched pattern again
        gui.update_display_status_logic("GitHub - Issues")
        gui.status_label.config.assert_called_with(text="GitHub (+10)")

    def test_status_label_shows_window_title_exactly_max_length(self):
        """Test that window title with exactly MAX_WINDOW_TITLE_LENGTH characters is not truncated."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with exactly MAX_WINDOW_TITLE_LENGTH characters
        title_max_chars = "a" * MAX_WINDOW_TITLE_LENGTH
        gui.update_display_status_logic(title_max_chars)

        # Verify status label shows full window title without ellipsis
        gui.status_label.config.assert_called_with(text=f"No match: {title_max_chars} (-1)")


if __name__ == "__main__":
    unittest.main()
