#!/usr/bin/env python3
"""Tests for GUI module - flow mode elapsed seconds display."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

try:
    from tests.gui_mock_base import Config, MockScoreDisplayWithStatusLabel, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import Config, MockScoreDisplayWithStatusLabel, ScoreTracker


class TestFlowModeDisplay(unittest.TestCase):
    """Test cases for flow mode elapsed seconds display."""

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

    def test_flow_mode_seconds_displayed_when_in_flow_state(self):
        """Test that flow mode elapsed seconds are displayed when in flow state."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state at 10:00:00
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.update_display_status_logic("GitHub - Repository")

        # Check display after 15 seconds (at 10:00:15)
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 15)
            # Update again to trigger display refresh
            gui.update_display_status_logic("GitHub - Repository")

        # Verify status label shows flow mode elapsed seconds
        gui.status_label.config.assert_called_with(text="GitHub (+10) [フロー: 15秒]")

    def test_flow_mode_seconds_not_displayed_when_not_in_flow_state(self):
        """Test that flow mode elapsed seconds are not displayed when not in flow state."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
default_score = 0

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

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.update_display_status_logic("GitHub - Repository")

        # Wait 10 seconds
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            gui.update_display_status_logic("GitHub - Repository")

        # Verify flow mode is active
        gui.status_label.config.assert_called_with(text="GitHub (+10) [フロー: 10秒]")

        # Exit flow state by decreasing score
        gui.update_display_status_logic("Twitter - Feed")

        # Verify flow mode time is not displayed (should show window elapsed time instead)
        # Since we just switched windows, window elapsed should be 0
        gui.status_label.config.assert_called_with(text="Twitter (-5)")

    def test_flow_mode_seconds_prioritized_over_window_elapsed(self):
        """Test that flow mode seconds take priority over window elapsed seconds."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state at 10:00:00
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.update_display_status_logic("GitHub - Repository")

        # Check after 20 seconds - flow mode time should be shown
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 20)
            gui.update_display_status_logic("GitHub - Repository")

        # Both window and flow mode have elapsed 20 seconds, but flow mode should be shown
        gui.status_label.config.assert_called_with(text="GitHub (+10) [フロー: 20秒]")

    def test_flow_mode_display_with_no_match(self):
        """Test flow mode display when no pattern matches but score increases due to default_score."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
default_score = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Start with positive default score (enters flow state)
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.update_display_status_logic("Random Window")

        # Check after 8 seconds
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 8)
            gui.update_display_status_logic("Random Window")

        # Should show flow mode time with "No match" text
        gui.status_label.config.assert_called_with(text="No match: Random Window (+1) [フロー: 8秒]")

    def test_flow_mode_seconds_resets_when_reentering_flow_state(self):
        """Test that flow mode elapsed seconds reset when exiting and reentering flow state."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
default_score = 0

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

        # Enter flow state at 10:00:00
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.update_display_status_logic("GitHub - Repository")

        # Stay in flow for 30 seconds
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 30)
            gui.update_display_status_logic("GitHub - Repository")
        gui.status_label.config.assert_called_with(text="GitHub (+10) [フロー: 30秒]")

        # Exit flow state at 10:00:35
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 35)
            gui.update_display_status_logic("Twitter - Feed")

        # Re-enter flow state at 10:00:40
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 40)
            gui.update_display_status_logic("GitHub - Issues")

        # Check after 10 seconds in new flow state (at 10:00:50)
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 50)
            gui.update_display_status_logic("GitHub - Issues")

        # Should show 10 seconds, not 30 or 50
        gui.status_label.config.assert_called_with(text="GitHub (+10) [フロー: 10秒]")


if __name__ == "__main__":
    unittest.main()
