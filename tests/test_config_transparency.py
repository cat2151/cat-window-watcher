#!/usr/bin/env python3
"""Tests for config module - transparency and print config settings."""

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
verbose = true
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
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 3
flow_mode_fade_rate_percent_per_second = 20
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
            _ = Config(str(self.config_path), verbose=False)
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
            self.assertIn("fade_window_on_flow_mode_enabled: True", output)
            self.assertIn("flow_mode_delay_seconds: 3", output)
            self.assertIn("flow_mode_fade_rate_percent_per_second: 20", output)
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
verbose = true

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
            _ = Config(str(self.config_path), verbose=False)
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
verbose = true
default_score = 0
"""
        self.config_path.write_text(config_content)

        # Capture stdout to verify output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        try:
            _ = Config(str(self.config_path), verbose=False)
            output = captured_output.getvalue()

            # Verify output indicates no patterns
            self.assertIn("No patterns defined", output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    unittest.main()
