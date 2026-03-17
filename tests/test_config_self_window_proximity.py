#!/usr/bin/env python3
"""Tests for config module - self window score and proximity settings."""

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


class TestConfigSelfWindow(unittest.TestCase):
    """Test cases for self_window_score configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

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


class TestConfigProximity(unittest.TestCase):
    """Test cases for proximity and always_on_top_while_score_decreasing configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

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


if __name__ == "__main__":
    unittest.main()
