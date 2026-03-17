#!/usr/bin/env python3
"""Tests for GUI module - window transparency updates."""

import shutil
import tempfile
import unittest
from pathlib import Path

try:
    from tests.gui_mock_base import Config, MockScoreDisplayWithTransparency, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import Config, MockScoreDisplayWithTransparency, ScoreTracker


class TestGuiTransparencyUpdate(unittest.TestCase):
    """Test cases for GUI window transparency updates in flow mode."""

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
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        score_tracker = ScoreTracker(patterns, default_score=0)
        gui = MockScoreDisplayWithTransparency(score_tracker, config)
        return gui

    def test_transparency_disabled_stays_opaque(self):
        """Test that transparency stays at 1.0 when fade mode is disabled."""
        config_content = """
fade_window_on_flow_mode_enabled = false
flow_mode_delay_seconds = 5
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        gui.score_tracker.update("github.com")
        self.assertTrue(gui.score_tracker.is_in_flow_state())

        # Update transparency
        gui._update_window_transparency()

        # Should remain fully opaque
        self.assertEqual(gui._current_transparency, 1.0)
        self.assertFalse(gui._fade_active)

    def test_transparency_fade_activates_after_delay(self):
        """Test that fade activates after flow state duration exceeds delay."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 5
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")
            self.assertTrue(gui.score_tracker.is_in_flow_state())

        # Before delay: should not fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 3)
            gui._update_window_transparency()
            self.assertEqual(gui._current_transparency, 1.0)
            self.assertFalse(gui._fade_active)

        # After delay: should start fading
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 6)
            gui._update_window_transparency()
            self.assertTrue(gui._fade_active)
            # With 10% fade rate and 1000ms interval, should fade 10% per update
            self.assertAlmostEqual(gui._current_transparency, 0.9, delta=0.01)

    def test_transparency_calculation_correct_fade_rate(self):
        """Test that transparency decreases at correct fade rate."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 20

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")

        # First update: 20% fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 1)
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.8, delta=0.01)

        # Second update: another 20% fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 2)
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.6, delta=0.01)

    def test_transparency_resets_on_exit_flow_state(self):
        """Test that transparency resets to 1.0 when exiting flow state."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -20
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state and fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.9, delta=0.01)

        # Exit flow state
        gui.score_tracker.update("twitter.com")
        self.assertFalse(gui.score_tracker.is_in_flow_state())

        # Transparency should reset
        gui._update_window_transparency()
        self.assertEqual(gui._current_transparency, 1.0)
        self.assertFalse(gui._fade_active)
        gui.root.attributes.assert_called_with("-alpha", 1.0)

    def test_transparency_minimum_zero(self):
        """Test that transparency doesn't go below 0.0."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")

        # Multiple updates with 100% fade rate should reach 0.0 and stay there
        for i in range(1, 5):
            with patch("src.score_tracker.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, i)
                gui._update_window_transparency()

        self.assertEqual(gui._current_transparency, 0.0)

    def test_transparency_update_interval_affects_fade(self):
        """Test that update interval affects fade calculation."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)
        gui.update_interval = 500  # 500ms instead of 1000ms

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")

        # With 500ms interval and 10% per second, should fade 5% per update
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 1)
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.95, delta=0.01)

    def test_transparency_no_change_when_already_at_target(self):
        """Test that transparency doesn't change when already at target state."""
        config_content = """
fade_window_on_flow_mode_enabled = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Reset mock after initialization
        gui.root.reset_mock()

        # Already at default transparency, mode disabled
        gui._update_window_transparency()

        # Should not call attributes if no change
        gui.root.attributes.assert_not_called()


class TestGuiDefaultTransparency(unittest.TestCase):
    """Test cases for GUI default transparency setting."""

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
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        score_tracker = ScoreTracker(patterns, default_score=0)
        gui = MockScoreDisplayWithTransparency(score_tracker, config)
        return gui

    def test_default_transparency_initializes_to_1_0_by_default(self):
        """Test that default transparency is 1.0 when not specified in config."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Verify default transparency is 1.0
        self.assertEqual(gui._current_transparency, 1.0)
        # Verify it's set on the window
        gui.root.attributes.assert_called_with("-alpha", 1.0)

    def test_default_transparency_initializes_to_configured_value(self):
        """Test that default transparency uses configured value."""
        config_content = """
default_transparency = 0.7

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Verify default transparency is 0.7
        self.assertEqual(gui._current_transparency, 0.7)
        # Verify it's set on the window
        gui.root.attributes.assert_called_with("-alpha", 0.7)

    def test_default_transparency_zero_fully_transparent(self):
        """Test that default transparency 0.0 makes window fully transparent."""
        config_content = """
default_transparency = 0.0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Verify default transparency is 0.0
        self.assertEqual(gui._current_transparency, 0.0)
        # Verify it's set on the window
        gui.root.attributes.assert_called_with("-alpha", 0.0)

    def test_default_transparency_half_transparent(self):
        """Test that default transparency 0.5 makes window half transparent."""
        config_content = """
default_transparency = 0.5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Verify default transparency is 0.5
        self.assertEqual(gui._current_transparency, 0.5)
        # Verify it's set on the window
        gui.root.attributes.assert_called_with("-alpha", 0.5)

    def test_transparency_resets_to_configured_default_not_1_0(self):
        """Test that transparency resets to configured default, not hardcoded 1.0."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 10
default_transparency = 0.8

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -20
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Initial transparency should be 0.8
        self.assertEqual(gui._current_transparency, 0.8)

        # Enter flow state and fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")
            gui._update_window_transparency()
            # Should fade to 0.7 (0.8 - 10%)
            self.assertAlmostEqual(gui._current_transparency, 0.7, delta=0.01)

        # Exit flow state
        gui.score_tracker.update("twitter.com")
        self.assertFalse(gui.score_tracker.is_in_flow_state())

        # Transparency should reset to default (0.8), not 1.0
        gui._update_window_transparency()
        self.assertEqual(gui._current_transparency, 0.8)
        # Verify the attributes call
        gui.root.attributes.assert_called_with("-alpha", 0.8)

    def test_transparency_disabled_flow_mode_restores_to_default(self):
        """Test that transparency restores to configured default when flow mode is disabled."""
        config_content = """
fade_window_on_flow_mode_enabled = false
default_transparency = 0.9

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Manually set transparency lower than default
        gui._current_transparency = 0.5

        # Update transparency with flow mode disabled
        gui._update_window_transparency()

        # Should restore to default (0.9)
        self.assertEqual(gui._current_transparency, 0.9)
        gui.root.attributes.assert_called_with("-alpha", 0.9)

    def test_transparency_with_various_default_values(self):
        """Test transparency initialization with various default values."""
        test_values = [0.0, 0.25, 0.5, 0.75, 1.0]

        for value in test_values:
            with self.subTest(value=value):
                config_content = f"""
default_transparency = {value}

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
                gui = self._create_mock_gui(config_content)

                # Verify transparency is set correctly
                self.assertEqual(gui._current_transparency, value)


if __name__ == "__main__":
    unittest.main()
