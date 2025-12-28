#!/usr/bin/env python3
"""Tests for config module."""

import tempfile
import time
import unittest
from pathlib import Path

try:
    from src.config import Config
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_load_valid_config(self):
        """Test loading a valid configuration file."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        patterns = config.get_window_patterns()

        self.assertEqual(len(patterns), 2)
        self.assertEqual(patterns[0]["regex"], "github")
        self.assertEqual(patterns[0]["score"], 10)
        self.assertEqual(patterns[0]["description"], "GitHub")
        self.assertEqual(patterns[1]["regex"], "twitter")
        self.assertEqual(patterns[1]["score"], -5)

    def test_load_empty_patterns(self):
        """Test loading config with no patterns."""
        config_content = """
# Empty config
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        patterns = config.get_window_patterns()

        self.assertEqual(len(patterns), 0)

    def test_missing_config_file(self):
        """Test handling of missing configuration file."""
        with self.assertRaises(SystemExit):
            Config("/nonexistent/config.toml")

    def test_config_with_missing_fields(self):
        """Test configuration with missing optional fields."""
        config_content = """
[[window_patterns]]
regex = "test"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        patterns = config.get_window_patterns()

        self.assertEqual(len(patterns), 1)
        self.assertEqual(patterns[0]["regex"], "test")
        self.assertEqual(patterns[0]["score"], 0)
        self.assertEqual(patterns[0]["description"], "")

    def test_default_score_loading(self):
        """Test loading default_score from configuration."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_default_score(), -1)

    def test_default_score_default_value(self):
        """Test default_score defaults to -1 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_default_score(), -1)

    def test_default_score_positive_value(self):
        """Test default_score with positive value."""
        config_content = """
default_score = 5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_default_score(), 5)

    def test_default_score_zero(self):
        """Test default_score explicitly set to zero."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_default_score(), 0)

    def test_apply_default_score_mode_default(self):
        """Test apply_default_score_mode defaults to True when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertTrue(config.get_apply_default_score_mode())

    def test_apply_default_score_mode_true(self):
        """Test apply_default_score_mode set to true."""
        config_content = """
apply_default_score_mode = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertTrue(config.get_apply_default_score_mode())

    def test_apply_default_score_mode_false(self):
        """Test apply_default_score_mode explicitly set to false."""
        config_content = """
apply_default_score_mode = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertFalse(config.get_apply_default_score_mode())

    def test_apply_default_score_mode_invalid_string(self):
        """Test apply_default_score_mode with string value raises SystemExit."""
        config_content = """
apply_default_score_mode = "true"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_apply_default_score_mode_invalid_integer(self):
        """Test apply_default_score_mode with integer value raises SystemExit."""
        config_content = """
apply_default_score_mode = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_always_on_top_default(self):
        """Test always_on_top defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertFalse(config.get_always_on_top())

    def test_always_on_top_true(self):
        """Test always_on_top set to true."""
        config_content = """
always_on_top = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertTrue(config.get_always_on_top())

    def test_always_on_top_false(self):
        """Test always_on_top explicitly set to false."""
        config_content = """
always_on_top = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertFalse(config.get_always_on_top())

    def test_always_on_top_reloaded_on_config_change(self):
        """Test that always_on_top is reloaded when config file changes."""
        config_content = """
always_on_top = false
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Verify initial config
        self.assertFalse(config.get_always_on_top())

        # Modify the file to change always_on_top
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
always_on_top = true
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify always_on_top was updated
        self.assertTrue(config.get_always_on_top())

    def test_is_modified_detects_changes(self):
        """Test that is_modified() detects file changes."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Initially, file should not be modified
        self.assertFalse(config.is_modified())

        # Modify the file
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
default_score = 5

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        self.config_path.write_text(new_content)

        # Now file should be detected as modified
        self.assertTrue(config.is_modified())

    def test_reload_if_modified_reloads_config(self):
        """Test that reload_if_modified() reloads the configuration."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Verify initial config
        self.assertEqual(config.get_default_score(), -1)
        self.assertEqual(len(config.get_window_patterns()), 1)
        self.assertEqual(config.get_window_patterns()[0]["regex"], "github")

        # Modify the file
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
default_score = 5

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"

[[window_patterns]]
regex = "facebook"
score = -3
description = "Facebook"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify new config was loaded
        self.assertEqual(config.get_default_score(), 5)
        self.assertEqual(len(config.get_window_patterns()), 2)
        self.assertEqual(config.get_window_patterns()[0]["regex"], "twitter")
        self.assertEqual(config.get_window_patterns()[1]["regex"], "facebook")

    def test_reload_if_modified_returns_false_when_not_modified(self):
        """Test that reload_if_modified() returns False when file not modified."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Call reload_if_modified without modifying file
        reloaded = config.reload_if_modified()
        self.assertFalse(reloaded)

    def test_is_modified_handles_missing_file(self):
        """Test that is_modified() handles missing file gracefully."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Remove the config file
        self.config_path.unlink()

        # is_modified should return False when file doesn't exist
        self.assertFalse(config.is_modified())

    def test_reload_if_modified_handles_invalid_toml(self):
        """Test that reload_if_modified() handles invalid TOML gracefully."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Verify initial config
        self.assertEqual(config.get_default_score(), -1)
        self.assertEqual(len(config.get_window_patterns()), 1)
        self.assertEqual(config.get_window_patterns()[0]["regex"], "github")

        # Modify the file with invalid TOML
        time.sleep(0.01)  # Ensure timestamp changes
        invalid_toml = """
default_score = -1
[invalid toml syntax here
regex = "twitter"
"""
        self.config_path.write_text(invalid_toml)

        # Reload should fail and return False
        reloaded = config.reload_if_modified()
        self.assertFalse(reloaded)

        # Old configuration should be preserved
        self.assertEqual(config.get_default_score(), -1)
        self.assertEqual(len(config.get_window_patterns()), 1)
        self.assertEqual(config.get_window_patterns()[0]["regex"], "github")

    def test_hide_on_mouse_proximity_default(self):
        """Test hide_on_mouse_proximity defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertFalse(config.get_hide_on_mouse_proximity())

    def test_hide_on_mouse_proximity_true(self):
        """Test hide_on_mouse_proximity set to true."""
        config_content = """
hide_on_mouse_proximity = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertTrue(config.get_hide_on_mouse_proximity())

    def test_hide_on_mouse_proximity_false(self):
        """Test hide_on_mouse_proximity explicitly set to false."""
        config_content = """
hide_on_mouse_proximity = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertFalse(config.get_hide_on_mouse_proximity())

    def test_proximity_distance_default(self):
        """Test proximity_distance defaults to 50 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_proximity_distance(), 50)

    def test_proximity_distance_custom_value(self):
        """Test proximity_distance with custom value."""
        config_content = """
proximity_distance = 100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_proximity_distance(), 100)

    def test_proximity_distance_zero(self):
        """Test proximity_distance explicitly set to zero."""
        config_content = """
proximity_distance = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_proximity_distance(), 0)

    def test_proximity_distance_invalid_negative(self):
        """Test proximity_distance with negative value raises SystemExit."""
        config_content = """
proximity_distance = -10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_proximity_distance_invalid_float(self):
        """Test proximity_distance with float value raises SystemExit."""
        config_content = """
proximity_distance = 50.5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_proximity_distance_invalid_string(self):
        """Test proximity_distance with string value raises SystemExit."""
        config_content = """
proximity_distance = "fifty"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_hide_on_mouse_proximity_reloaded_on_config_change(self):
        """Test that hide_on_mouse_proximity is reloaded when config file changes."""
        config_content = """
hide_on_mouse_proximity = false
always_on_top = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Verify initial config
        self.assertFalse(config.get_hide_on_mouse_proximity())

        # Modify the file to change hide_on_mouse_proximity
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
hide_on_mouse_proximity = true
always_on_top = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify hide_on_mouse_proximity was updated
        self.assertTrue(config.get_hide_on_mouse_proximity())

    def test_proximity_distance_reloaded_on_config_change(self):
        """Test that proximity_distance is reloaded when config file changes."""
        config_content = """
proximity_distance = 50

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Verify initial config
        self.assertEqual(config.get_proximity_distance(), 50)

        # Modify the file to change proximity_distance
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
proximity_distance = 150

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify proximity_distance was updated
        self.assertEqual(config.get_proximity_distance(), 150)

    def test_all_proximity_settings_together(self):
        """Test loading all proximity-related settings together."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 75

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertTrue(config.get_always_on_top())
        self.assertTrue(config.get_hide_on_mouse_proximity())
        self.assertEqual(config.get_proximity_distance(), 75)


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

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

    def test_mild_penalty_start_hour_default(self):
        """Test mild_penalty_start_hour defaults to 22 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

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

        config = Config(str(self.config_path))
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
        config = Config(str(self.config_path))

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
        """Test reset_score_every_30_minutes defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertFalse(config.get_reset_score_every_30_minutes())

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

        config = Config(str(self.config_path))
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

        config = Config(str(self.config_path))
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
            Config(str(self.config_path))

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
            Config(str(self.config_path))

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
        config = Config(str(self.config_path))

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
