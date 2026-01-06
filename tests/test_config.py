#!/usr/bin/env python3
"""Tests for config module."""

import io
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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
            Config(str(self.config_path), verbose=False)

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
            Config(str(self.config_path), verbose=False)

    def test_self_window_score_default(self):
        """Test self_window_score defaults to 0 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_self_window_score(), 0)

    def test_self_window_score_positive(self):
        """Test self_window_score set to positive value."""
        config_content = """
self_window_score = 5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_self_window_score(), 5)

    def test_self_window_score_negative(self):
        """Test self_window_score set to negative value."""
        config_content = """
self_window_score = -2

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_self_window_score(), -2)

    def test_self_window_score_zero(self):
        """Test self_window_score explicitly set to zero."""
        config_content = """
self_window_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_self_window_score(), 0)

    def test_self_window_score_reloaded_on_config_change(self):
        """Test that self_window_score is reloaded when config file changes."""
        config_content = """
self_window_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertEqual(config.get_self_window_score(), 0)

        # Modify the file to change self_window_score
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
self_window_score = 3

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify self_window_score was updated
        self.assertEqual(config.get_self_window_score(), 3)

    def test_self_window_score_invalid_string(self):
        """Test self_window_score with string value raises SystemExit."""
        config_content = """
self_window_score = "zero"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_self_window_score_invalid_float(self):
        """Test self_window_score with float value raises SystemExit."""
        config_content = """
self_window_score = 1.5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_always_on_top_default(self):
        """Test always_on_top defaults to True when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_always_on_top())

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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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
        config = Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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
        """Test hide_on_mouse_proximity defaults to True when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_hide_on_mouse_proximity())

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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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

        config = Config(str(self.config_path), verbose=False)
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
            Config(str(self.config_path), verbose=False)

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
            Config(str(self.config_path), verbose=False)

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
            Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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
        config = Config(str(self.config_path), verbose=False)

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

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_always_on_top())
        self.assertTrue(config.get_hide_on_mouse_proximity())
        self.assertEqual(config.get_proximity_distance(), 75)

    def test_always_on_top_while_score_decreasing_default(self):
        """Test always_on_top_while_score_decreasing defaults to True when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_always_on_top_while_score_decreasing())

    def test_always_on_top_while_score_decreasing_true(self):
        """Test always_on_top_while_score_decreasing set to true."""
        config_content = """
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_always_on_top_while_score_decreasing())

    def test_always_on_top_while_score_decreasing_false(self):
        """Test always_on_top_while_score_decreasing explicitly set to false."""
        config_content = """
always_on_top_while_score_decreasing = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_always_on_top_while_score_decreasing())

    def test_always_on_top_while_score_decreasing_invalid_string(self):
        """Test always_on_top_while_score_decreasing with string value raises SystemExit."""
        config_content = """
always_on_top_while_score_decreasing = "yes"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_always_on_top_while_score_decreasing_invalid_integer(self):
        """Test always_on_top_while_score_decreasing with integer value raises SystemExit."""
        config_content = """
always_on_top_while_score_decreasing = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)


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


class TestFlowModeConfig(unittest.TestCase):
    """Test cases for flow mode configuration settings."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_fade_window_on_flow_mode_enabled_default(self):
        """Test fade_window_on_flow_mode_enabled defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_fade_window_on_flow_mode_enabled())

    def test_fade_window_on_flow_mode_enabled_true(self):
        """Test fade_window_on_flow_mode_enabled set to true."""
        config_content = """
fade_window_on_flow_mode_enabled = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_fade_window_on_flow_mode_enabled())

    def test_fade_window_on_flow_mode_enabled_false(self):
        """Test fade_window_on_flow_mode_enabled explicitly set to false."""
        config_content = """
fade_window_on_flow_mode_enabled = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_fade_window_on_flow_mode_enabled())

    def test_fade_window_on_flow_mode_enabled_invalid_string(self):
        """Test fade_window_on_flow_mode_enabled with string value raises SystemExit."""
        config_content = """
fade_window_on_flow_mode_enabled = "yes"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_flow_mode_delay_seconds_default(self):
        """Test flow_mode_delay_seconds defaults to 10 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_delay_seconds(), 10)

    def test_flow_mode_delay_seconds_custom_value(self):
        """Test flow_mode_delay_seconds with custom value."""
        config_content = """
flow_mode_delay_seconds = 20

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_delay_seconds(), 20)

    def test_flow_mode_delay_seconds_zero(self):
        """Test flow_mode_delay_seconds can be set to zero."""
        config_content = """
flow_mode_delay_seconds = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_delay_seconds(), 0)

    def test_flow_mode_delay_seconds_negative(self):
        """Test flow_mode_delay_seconds with negative value raises SystemExit."""
        config_content = """
flow_mode_delay_seconds = -5
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_flow_mode_delay_seconds_invalid_float(self):
        """Test flow_mode_delay_seconds with float value raises SystemExit."""
        config_content = """
flow_mode_delay_seconds = 10.5
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_flow_mode_fade_rate_default(self):
        """Test flow_mode_fade_rate_percent_per_second defaults to 1 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_fade_rate_percent_per_second(), 1)

    def test_flow_mode_fade_rate_custom_value(self):
        """Test flow_mode_fade_rate_percent_per_second with custom value."""
        config_content = """
flow_mode_fade_rate_percent_per_second = 5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_fade_rate_percent_per_second(), 5)

    def test_flow_mode_fade_rate_max_value(self):
        """Test flow_mode_fade_rate_percent_per_second can be set to 100."""
        config_content = """
flow_mode_fade_rate_percent_per_second = 100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_fade_rate_percent_per_second(), 100)

    def test_flow_mode_fade_rate_zero(self):
        """Test flow_mode_fade_rate_percent_per_second with zero raises SystemExit."""
        config_content = """
flow_mode_fade_rate_percent_per_second = 0
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_flow_mode_fade_rate_negative(self):
        """Test flow_mode_fade_rate_percent_per_second with negative value raises SystemExit."""
        config_content = """
flow_mode_fade_rate_percent_per_second = -1
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_flow_mode_fade_rate_over_100(self):
        """Test flow_mode_fade_rate_percent_per_second with value over 100 raises SystemExit."""
        config_content = """
flow_mode_fade_rate_percent_per_second = 101
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_all_flow_mode_settings_together(self):
        """Test loading all flow mode settings together."""
        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 15
flow_mode_fade_rate_percent_per_second = 2

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_fade_window_on_flow_mode_enabled())
        self.assertEqual(config.get_flow_mode_delay_seconds(), 15)
        self.assertEqual(config.get_flow_mode_fade_rate_percent_per_second(), 2)

    def test_flow_mode_settings_reload_on_config_change(self):
        """Test that flow mode settings are reloaded when config file changes."""
        config_content = """
fade_window_on_flow_mode_enabled = false
flow_mode_delay_seconds = 10
flow_mode_fade_rate_percent_per_second = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_fade_window_on_flow_mode_enabled())
        self.assertEqual(config.get_flow_mode_delay_seconds(), 10)

        # Wait a bit to ensure file modification time changes
        time.sleep(0.1)

        # Modify config file
        new_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 20
flow_mode_fade_rate_percent_per_second = 5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify settings were updated
        self.assertTrue(config.get_fade_window_on_flow_mode_enabled())
        self.assertEqual(config.get_flow_mode_delay_seconds(), 20)
        self.assertEqual(config.get_flow_mode_fade_rate_percent_per_second(), 5)


class TestWindowPositionConfig(unittest.TestCase):
    """Test cases for window position configuration settings."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_window_x_default(self):
        """Test window_x defaults to None when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertIsNone(config.get_window_x())

    def test_window_y_default(self):
        """Test window_y defaults to None when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertIsNone(config.get_window_y())

    def test_window_x_positive_value(self):
        """Test window_x with positive value."""
        config_content = """
window_x = 100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_x(), 100)

    def test_window_y_positive_value(self):
        """Test window_y with positive value."""
        config_content = """
window_y = 200

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_y(), 200)

    def test_window_x_zero(self):
        """Test window_x with zero value."""
        config_content = """
window_x = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_x(), 0)

    def test_window_y_zero(self):
        """Test window_y with zero value."""
        config_content = """
window_y = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_y(), 0)

    def test_window_x_negative_value(self):
        """Test window_x with negative value (valid for multi-monitor setups)."""
        config_content = """
window_x = -100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_x(), -100)

    def test_window_y_negative_value(self):
        """Test window_y with negative value (valid for multi-monitor setups)."""
        config_content = """
window_y = -50

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_y(), -50)

    def test_window_x_invalid_float(self):
        """Test window_x with float value raises SystemExit."""
        config_content = """
window_x = 100.5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_window_y_invalid_float(self):
        """Test window_y with float value raises SystemExit."""
        config_content = """
window_y = 200.7

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_window_x_invalid_string(self):
        """Test window_x with string value raises SystemExit."""
        config_content = """
window_x = "100"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_window_y_invalid_string(self):
        """Test window_y with string value raises SystemExit."""
        config_content = """
window_y = "200"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_both_window_position_settings(self):
        """Test loading both window_x and window_y together."""
        config_content = """
window_x = 150
window_y = 250

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_x(), 150)
        self.assertEqual(config.get_window_y(), 250)

    def test_window_position_reloaded_on_config_change(self):
        """Test that window position settings are reloaded when config file changes."""
        config_content = """
window_x = 100
window_y = 200

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertEqual(config.get_window_x(), 100)
        self.assertEqual(config.get_window_y(), 200)

        # Modify the file to change window position
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
window_x = 300
window_y = 400

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify window position settings were updated
        self.assertEqual(config.get_window_x(), 300)
        self.assertEqual(config.get_window_y(), 400)

    def test_window_x_only_without_y(self):
        """Test setting window_x without window_y."""
        config_content = """
window_x = 100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_window_x(), 100)
        self.assertIsNone(config.get_window_y())

    def test_window_y_only_without_x(self):
        """Test setting window_y without window_x."""
        config_content = """
window_y = 200

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertIsNone(config.get_window_x())
        self.assertEqual(config.get_window_y(), 200)


class TestDefaultTransparencyConfig(unittest.TestCase):
    """Test cases for default_transparency configuration settings."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_default_transparency_default(self):
        """Test default_transparency defaults to 1.0 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 1.0)

    def test_default_transparency_custom_value(self):
        """Test default_transparency with custom value."""
        config_content = """
default_transparency = 0.8

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 0.8)

    def test_default_transparency_zero(self):
        """Test default_transparency can be set to zero (fully transparent)."""
        config_content = """
default_transparency = 0.0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 0.0)

    def test_default_transparency_one(self):
        """Test default_transparency can be set to 1.0 (fully opaque)."""
        config_content = """
default_transparency = 1.0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 1.0)

    def test_default_transparency_integer_value(self):
        """Test default_transparency accepts integer values (0 or 1)."""
        config_content = """
default_transparency = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 1)

    def test_default_transparency_half(self):
        """Test default_transparency with 0.5 (half transparent)."""
        config_content = """
default_transparency = 0.5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 0.5)

    def test_default_transparency_invalid_negative(self):
        """Test default_transparency with negative value raises SystemExit."""
        config_content = """
default_transparency = -0.1
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_default_transparency_invalid_over_one(self):
        """Test default_transparency with value over 1.0 raises SystemExit."""
        config_content = """
default_transparency = 1.1
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_default_transparency_invalid_string(self):
        """Test default_transparency with string value raises SystemExit."""
        config_content = """
default_transparency = "opaque"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_default_transparency_reloaded_on_config_change(self):
        """Test that default_transparency is reloaded when config file changes."""
        config_content = """
default_transparency = 1.0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertEqual(config.get_default_transparency(), 1.0)

        # Modify the file to change default_transparency
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
default_transparency = 0.6

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify default_transparency was updated
        self.assertEqual(config.get_default_transparency(), 0.6)

    def test_default_transparency_boundary_values(self):
        """Test default_transparency with exact boundary values."""
        # Test lower boundary (0.0)
        config_content_low = """
default_transparency = 0.0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content_low)
        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_default_transparency(), 0.0)

        # Test upper boundary (1.0)
        time.sleep(0.01)  # Ensure timestamp changes
        config_content_high = """
default_transparency = 1.0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content_high)
        config.reload_if_modified()
        self.assertEqual(config.get_default_transparency(), 1.0)


class TestPrintConfig(unittest.TestCase):
    """Test cases for print_config method."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_print_config_outputs_all_settings(self):
        """Test that print_config outputs all configuration settings."""
        config_content = """
default_score = -1
apply_default_score_mode = true
self_window_score = 0
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50
always_on_top_while_score_decreasing = true
mild_penalty_mode = false
mild_penalty_start_hour = 22
mild_penalty_end_hour = 23
score_up_color = "#ffffff"
score_down_color = "#ff0000"
reset_score_every_30_minutes = true
fade_window_on_flow_mode_enabled = false
flow_mode_delay_seconds = 10
flow_mode_fade_rate_percent_per_second = 1
default_transparency = 1.0
window_x = 100
window_y = 200

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

        # Capture stdout to verify output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            _ = Config(str(self.config_path), verbose=True)
            output = captured_output.getvalue()

            # Verify that key settings are printed
            self.assertIn("現在の設定値", output)
            self.assertIn("default_score: -1", output)
            self.assertIn("apply_default_score_mode: True", output)
            self.assertIn("self_window_score: 0", output)
            self.assertIn("always_on_top: True", output)
            self.assertIn("hide_on_mouse_proximity: True", output)
            self.assertIn("proximity_distance: 50", output)
            self.assertIn("always_on_top_while_score_decreasing: True", output)
            self.assertIn("mild_penalty_mode: False", output)
            self.assertIn("mild_penalty_start_hour: 22", output)
            self.assertIn("mild_penalty_end_hour: 23", output)
            self.assertIn("score_up_color: #ffffff", output)
            self.assertIn("score_down_color: #ff0000", output)
            self.assertIn("reset_score_every_30_minutes: True", output)
            self.assertIn("fade_window_on_flow_mode_enabled: False", output)
            self.assertIn("flow_mode_delay_seconds: 10", output)
            self.assertIn("flow_mode_fade_rate_percent_per_second: 1", output)
            self.assertIn("default_transparency: 1.0", output)
            self.assertIn("window_x: 100", output)
            self.assertIn("window_y: 200", output)
            self.assertIn("[1] GitHub", output)
            self.assertIn("[2] Twitter", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_print_config_with_default_values(self):
        """Test that print_config outputs default values when not specified in config."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        # Capture stdout to verify output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            _ = Config(str(self.config_path), verbose=True)
            output = captured_output.getvalue()

            # Verify default values are printed
            self.assertIn("default_score: -1", output)  # default value
            self.assertIn("apply_default_score_mode: True", output)  # default value
            self.assertIn("self_window_score: 0", output)  # default value
            self.assertIn("always_on_top: True", output)  # default value
            self.assertIn("mild_penalty_mode: False", output)  # default value
            self.assertIn("window_x: None", output)  # default value (None)
            self.assertIn("window_y: None", output)  # default value (None)
        finally:
            sys.stdout = sys.__stdout__

    def test_print_config_with_no_patterns(self):
        """Test that print_config handles empty pattern list."""
        config_content = """
default_score = 0
"""
        self.config_path.write_text(config_content)

        # Capture stdout to verify output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            _ = Config(str(self.config_path), verbose=True)
            output = captured_output.getvalue()

            # Verify output indicates no patterns
            self.assertIn("No patterns defined", output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
