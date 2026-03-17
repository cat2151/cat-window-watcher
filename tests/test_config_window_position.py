#!/usr/bin/env python3
"""Tests for config module - window position and debug screensaver detection settings."""

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


class TestDebugScreensaverDetectionConfig(unittest.TestCase):
    """Test cases for debug_screensaver_detection configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        if hasattr(self, "temp_dir") and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_debug_screensaver_detection_default(self):
        """Test debug_screensaver_detection defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_debug_screensaver_detection())

    def test_debug_screensaver_detection_true(self):
        """Test debug_screensaver_detection set to true."""
        config_content = """
debug_screensaver_detection = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_debug_screensaver_detection())

    def test_debug_screensaver_detection_false(self):
        """Test debug_screensaver_detection explicitly set to false."""
        config_content = """
debug_screensaver_detection = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_debug_screensaver_detection())

    def test_debug_screensaver_detection_invalid_string(self):
        """Test debug_screensaver_detection with string value raises SystemExit."""
        config_content = """
debug_screensaver_detection = "true"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_debug_screensaver_detection_invalid_integer(self):
        """Test debug_screensaver_detection with integer value raises SystemExit."""
        config_content = """
debug_screensaver_detection = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_debug_screensaver_detection_reloaded_on_config_change(self):
        """Test that debug_screensaver_detection setting is reloaded when config file changes."""
        config_content = """
debug_screensaver_detection = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertFalse(config.get_debug_screensaver_detection())

        # Modify the file to change debug_screensaver_detection
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
debug_screensaver_detection = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify debug_screensaver_detection setting was updated
        self.assertTrue(config.get_debug_screensaver_detection())


if __name__ == "__main__":
    unittest.main()
