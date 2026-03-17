#!/usr/bin/env python3
"""Tests for config module - flow mode and verbose mode settings."""

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


class TestFlowModeConfig(unittest.TestCase):
    """Test cases for flow mode configuration settings."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_fade_window_on_flow_mode_enabled_default(self):
        """Test fade_window_on_flow_mode_enabled defaults to True when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_fade_window_on_flow_mode_enabled())

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
        """Test flow_mode_delay_seconds defaults to 3 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_delay_seconds(), 3)

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
        """Test flow_mode_fade_rate_percent_per_second defaults to 20 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertEqual(config.get_flow_mode_fade_rate_percent_per_second(), 20)

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
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 3
flow_mode_fade_rate_percent_per_second = 20

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertTrue(config.get_fade_window_on_flow_mode_enabled())
        self.assertEqual(config.get_flow_mode_delay_seconds(), 3)

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


class TestVerboseModeConfig(unittest.TestCase):
    """Test cases for verbose mode configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        if hasattr(self, "temp_dir") and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_verbose_default(self):
        """Test verbose defaults to False when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path), verbose=False)
        self.assertFalse(config.get_verbose())

    def test_verbose_true(self):
        """Test verbose set to true."""
        config_content = """
verbose = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        # Capture stdout to verify verbose output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            config = Config(str(self.config_path), verbose=False)
            self.assertTrue(config.get_verbose())
            output = captured_output.getvalue()
            # Verify that configuration was printed
            self.assertIn("現在の設定値", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_verbose_false(self):
        """Test verbose explicitly set to false."""
        config_content = """
verbose = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        # Capture stdout to verify no verbose output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            config = Config(str(self.config_path), verbose=False)
            self.assertFalse(config.get_verbose())
            output = captured_output.getvalue()
            # Verify that configuration was not printed
            self.assertNotIn("現在の設定値", output)
        finally:
            sys.stdout = sys.__stdout__

    def test_verbose_invalid_string(self):
        """Test verbose with string value raises SystemExit."""
        config_content = """
verbose = "true"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_verbose_invalid_integer(self):
        """Test verbose with integer value raises SystemExit."""
        config_content = """
verbose = 1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path), verbose=False)

    def test_verbose_reloaded_on_config_change(self):
        """Test that verbose setting is reloaded when config file changes."""
        config_content = """
verbose = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path), verbose=False)

        # Verify initial config
        self.assertFalse(config.get_verbose())

        # Modify the file to change verbose
        time.sleep(0.01)  # Ensure timestamp changes
        new_content = """
verbose = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(new_content)

        # Reload configuration
        reloaded = config.reload_if_modified()
        self.assertTrue(reloaded)

        # Verify verbose setting was updated
        self.assertTrue(config.get_verbose())


if __name__ == "__main__":
    unittest.main()
