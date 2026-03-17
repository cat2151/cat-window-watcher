#!/usr/bin/env python3
"""Tests for config module - mild penalty and reset score settings."""

import sys
import tempfile
import time
import unittest
from pathlib import Path

try:
    from src.config import Config
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config


class TestMildPenaltyModeConfig(unittest.TestCase):
    """Test cases for mild penalty mode configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_mild_penalty_mode_default(self):
        """Test mild_penalty_mode defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_mild_penalty_mode())

    def test_mild_penalty_mode_true(self):
        """Test mild_penalty_mode set to true."""
        config_content = """
mild_penalty_mode = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_mild_penalty_mode())

    def test_mild_penalty_mode_false(self):
        """Test mild_penalty_mode explicitly set to false."""
        config_content = """
mild_penalty_mode = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_mild_penalty_mode())

    def test_mild_penalty_mode_invalid_string(self):
        """Test mild_penalty_mode with string value raises SystemExit."""
        config_content = """
mild_penalty_mode = "true"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_mode_invalid_integer(self):
        """Test mild_penalty_mode with integer value raises SystemExit."""
        config_content = """
mild_penalty_mode = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_start_hour_default(self):
        """Test mild_penalty_start_hour defaults to 22 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_mild_penalty_start_hour(), 22)

    def test_mild_penalty_start_hour_custom_value(self):
        """Test mild_penalty_start_hour with custom value."""
        config_content = """
mild_penalty_start_hour = 20

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_mild_penalty_start_hour(), 20)

    def test_mild_penalty_end_hour_default(self):
        """Test mild_penalty_end_hour defaults to 23 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_mild_penalty_end_hour(), 23)

    def test_mild_penalty_end_hour_custom_value(self):
        """Test mild_penalty_end_hour with custom value."""
        config_content = """
mild_penalty_end_hour = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_mild_penalty_end_hour(), 1)

    def test_mild_penalty_hours_boundary_values(self):
        """Test mild penalty hours with boundary values (0 and 23)."""
        config_content = """
mild_penalty_start_hour = 0
mild_penalty_end_hour = 23

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_mild_penalty_start_hour(), 0)
        self.assertEqual(config.get_mild_penalty_end_hour(), 23)

    def test_mild_penalty_start_hour_invalid_negative(self):
        """Test mild_penalty_start_hour with negative value raises SystemExit."""
        config_content = """
mild_penalty_start_hour = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_start_hour_invalid_over_23(self):
        """Test mild_penalty_start_hour with value over 23 raises SystemExit."""
        config_content = """
mild_penalty_start_hour = 24

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_end_hour_invalid_negative(self):
        """Test mild_penalty_end_hour with negative value raises SystemExit."""
        config_content = """
mild_penalty_end_hour = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_end_hour_invalid_over_23(self):
        """Test mild_penalty_end_hour with value over 23 raises SystemExit."""
        config_content = """
mild_penalty_end_hour = 24

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_start_hour_invalid_float(self):
        """Test mild_penalty_start_hour with float value raises SystemExit."""
        config_content = """
mild_penalty_start_hour = 22.5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_mild_penalty_end_hour_invalid_string(self):
        """Test mild_penalty_end_hour with string value raises SystemExit."""
        config_content = """
mild_penalty_end_hour = "twenty-three"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_all_mild_penalty_settings_together(self):
        """Test loading all mild penalty settings together."""
        config_content = """
mild_penalty_mode = true
mild_penalty_start_hour = 22
mild_penalty_end_hour = 23

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_mild_penalty_mode())
        self.assertEqual(config.get_mild_penalty_start_hour(), 22)
        self.assertEqual(config.get_mild_penalty_end_hour(), 23)

    def test_mild_penalty_settings_reloaded_on_config_change(self):
        """Test that mild penalty settings are reloaded when config file changes."""
        config_content = """
mild_penalty_mode = false
mild_penalty_start_hour = 22
mild_penalty_end_hour = 23

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertFalse(config.get_mild_penalty_mode())
        self.assertEqual(config.get_mild_penalty_start_hour(), 22)
        self.assertEqual(config.get_mild_penalty_end_hour(), 23)

        # Modify the file to change mild penalty settings
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
mild_penalty_mode = true
mild_penalty_start_hour = 20
mild_penalty_end_hour = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify mild penalty settings were updated
        self.assertTrue(config.get_mild_penalty_mode())
        self.assertEqual(config.get_mild_penalty_start_hour(), 20)
        self.assertEqual(config.get_mild_penalty_end_hour(), 1)


class TestResetScoreEvery30MinutesConfig(unittest.TestCase):
    """Test cases for reset_score_every_30_minutes configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_reset_score_every_30_minutes_default(self):
        """Test reset_score_every_30_minutes defaults to True when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_reset_score_every_30_minutes())

    def test_reset_score_every_30_minutes_true(self):
        """Test reset_score_every_30_minutes set to true."""
        config_content = """
reset_score_every_30_minutes = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_reset_score_every_30_minutes())

    def test_reset_score_every_30_minutes_false(self):
        """Test reset_score_every_30_minutes explicitly set to false."""
        config_content = """
reset_score_every_30_minutes = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_reset_score_every_30_minutes())

    def test_reset_score_every_30_minutes_invalid_integer(self):
        """Test reset_score_every_30_minutes with integer value raises SystemExit."""
        config_content = """
reset_score_every_30_minutes = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_reset_score_every_30_minutes_invalid_string(self):
        """Test reset_score_every_30_minutes with string value raises SystemExit."""
        config_content = """
reset_score_every_30_minutes = "yes"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_reset_score_every_30_minutes_reloaded_on_config_change(self):
        """Test that reset_score_every_30_minutes is reloaded when config file changes."""
        config_content = """
reset_score_every_30_minutes = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertFalse(config.get_reset_score_every_30_minutes())

        # Modify the file to change reset_score_every_30_minutes
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
reset_score_every_30_minutes = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify reset_score_every_30_minutes was updated
        self.assertTrue(config.get_reset_score_every_30_minutes())


if __name__ == "__main__":
    unittest.main()
