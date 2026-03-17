#!/usr/bin/env python3
"""Tests for GUI module - clipboard copy on CTRL+C."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

try:
    from tests.gui_mock_base import Config, MockScoreDisplay, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import Config, MockScoreDisplay, ScoreTracker


class TestClipboardCopyOnCtrlC(unittest.TestCase):
    """Test cases for clipboard copy on CTRL+C key press functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_mock_gui(self, config_content):
        """Helper to create a mock GUI with given config."""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Create patterns for testing
        patterns = [{"regex": "github", "score": 10, "description": "GitHub"}]
        score_tracker = ScoreTracker(patterns)

        # Create mock GUI with clipboard methods
        gui = MockScoreDisplay(score_tracker, config)
        gui.score_label = MagicMock()
        gui.status_label = MagicMock()

        # Mock clipboard methods
        gui.root.clipboard_clear = MagicMock()
        gui.root.clipboard_append = MagicMock()
        gui.root.update = MagicMock()

        return gui

    def test_ctrl_c_copies_current_window_title(self):
        """Test that CTRL+C copies the previous window title to clipboard."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set a previous window title (this is what should be copied)
        gui._previous_window_title = "Random Window Title"
        # Set a different current window title (this should NOT be copied)
        gui._current_window_title = "Cat Window Watcher - Cat is watching you -"

        # Simulate CTRL+C press
        gui._on_ctrl_c(None)

        # Verify clipboard methods were called with previous title
        gui.root.clipboard_clear.assert_called_once()
        gui.root.clipboard_append.assert_called_once_with("Random Window Title")
        gui.root.update.assert_called_once()

    def test_ctrl_c_with_empty_title_does_not_copy(self):
        """Test that CTRL+C does not copy when previous window title is empty."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set empty previous window title
        gui._previous_window_title = ""
        # Set non-empty current window title (should not be copied)
        gui._current_window_title = "Some Window"

        # Simulate CTRL+C press
        gui._on_ctrl_c(None)

        # Verify clipboard methods were not called
        gui.root.clipboard_clear.assert_not_called()
        gui.root.clipboard_append.assert_not_called()

    def test_ctrl_c_handles_errors_gracefully(self):
        """Test that clipboard errors are handled gracefully without crashing."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set a previous window title
        gui._previous_window_title = "Random Window Title"

        # Make clipboard_append raise an exception
        gui.root.clipboard_append.side_effect = Exception("Clipboard error")

        # Simulate CTRL+C press - should not raise exception
        try:
            gui._on_ctrl_c(None)
        except Exception as e:
            self.fail(f"_on_ctrl_c raised exception: {e}")

        # Verify clipboard_clear was called before the error
        gui.root.clipboard_clear.assert_called_once()

    def test_ctrl_c_can_copy_multiple_times(self):
        """Test that CTRL+C can copy the same previous title multiple times."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set a previous window title
        gui._previous_window_title = "Random Window Title"

        # First CTRL+C
        gui._on_ctrl_c(None)
        gui.root.clipboard_clear.assert_called_once()
        gui.root.clipboard_append.assert_called_once_with("Random Window Title")

        # Reset mocks
        gui.root.clipboard_clear.reset_mock()
        gui.root.clipboard_append.reset_mock()
        gui.root.update.reset_mock()

        # Second CTRL+C with same title - should copy again
        gui._on_ctrl_c(None)
        gui.root.clipboard_clear.assert_called_once()
        gui.root.clipboard_append.assert_called_once_with("Random Window Title")

    def test_ctrl_c_copies_different_titles(self):
        """Test that CTRL+C copies different previous window titles correctly."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set first previous window title
        gui._previous_window_title = "First Window"

        # First CTRL+C
        gui._on_ctrl_c(None)
        gui.root.clipboard_append.assert_called_once_with("First Window")

        # Reset mocks
        gui.root.clipboard_clear.reset_mock()
        gui.root.clipboard_append.reset_mock()
        gui.root.update.reset_mock()

        # Change previous window title
        gui._previous_window_title = "Second Window"

        # Second CTRL+C with different title
        gui._on_ctrl_c(None)
        gui.root.clipboard_append.assert_called_once_with("Second Window")

    def test_ctrl_c_copies_previous_not_current_title(self):
        """Test that CTRL+C copies the previous window title, not the current one.

        This verifies the fix for issue #37: When user presses CTRL+C, the focus
        shifts to the app itself, so we want the previous window title
        (before the app became active), not the current one.
        """
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set different current and previous window titles
        gui._current_window_title = "Cat Window Watcher - Cat is watching you -"
        gui._previous_window_title = "GitHub - Pull Requests"

        # Simulate CTRL+C press
        gui._on_ctrl_c(None)

        # Verify that the previous title is copied, not the current one
        gui.root.clipboard_append.assert_called_once_with("GitHub - Pull Requests")
        # Make sure it's NOT the current title
        self.assertNotEqual(gui.root.clipboard_append.call_args[0][0], "Cat Window Watcher - Cat is watching you -")

    def test_ctrl_c_preserves_previous_title_when_current_becomes_empty(self):
        """Test that previous title is preserved when current title becomes empty.

        If window monitoring temporarily fails and returns an empty title,
        we should preserve the last valid previous title for clipboard operations.
        """
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Start with valid titles
        gui._previous_window_title = "GitHub - Pull Requests"
        gui._current_window_title = "Twitter - Home"

        # Simulate current title becoming empty (monitoring failure)
        # In the real implementation, this would happen through update_display
        # Here we test the clipboard behavior with preserved previous title
        new_previous = gui._current_window_title if gui._current_window_title else gui._previous_window_title
        gui._previous_window_title = new_previous
        gui._current_window_title = ""

        # Press CTRL+C - should still have the last valid title
        gui._on_ctrl_c(None)

        # Verify that we still have a valid title to copy
        gui.root.clipboard_append.assert_called_once_with("Twitter - Home")


if __name__ == "__main__":
    unittest.main()
