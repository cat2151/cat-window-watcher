#!/usr/bin/env python3
"""Tests for score color configuration."""

import tempfile
import unittest
from pathlib import Path

try:
    from src.config import Config
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config


class TestScoreColorConfig(unittest.TestCase):
    """Test cases for score color configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def test_score_color_defaults(self):
        """Test default score color values."""
        config_content = """
[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_score_up_color(), "#ffffff")
        self.assertEqual(config.get_score_down_color(), "#ff0000")

    def test_score_color_custom_values(self):
        """Test custom score color values."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#0000ff"

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_score_up_color(), "#00ff00")
        self.assertEqual(config.get_score_down_color(), "#0000ff")

    def test_score_up_color_invalid_not_string(self):
        """Test score_up_color with non-string value raises SystemExit."""
        config_content = """
score_up_color = 123456

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_score_down_color_invalid_not_string(self):
        """Test score_down_color with non-string value raises SystemExit."""
        config_content = """
score_down_color = 123456

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_score_up_color_invalid_no_hash(self):
        """Test score_up_color without # prefix raises SystemExit."""
        config_content = """
score_up_color = "ffffff"

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_score_down_color_invalid_no_hash(self):
        """Test score_down_color without # prefix raises SystemExit."""
        config_content = """
score_down_color = "ff0000"

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        self.config_path.write_text(config_content)

        with self.assertRaises(SystemExit):
            Config(str(self.config_path))

    def test_score_colors_with_other_settings(self):
        """Test score colors work with other configuration settings."""
        config_content = """
default_score = -1
always_on_top = true
score_up_color = "#ffff00"
score_down_color = "#ff00ff"

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
        self.assertEqual(config.get_score_up_color(), "#ffff00")
        self.assertEqual(config.get_score_down_color(), "#ff00ff")
        self.assertEqual(config.get_default_score(), -1)
        self.assertTrue(config.get_always_on_top())
        self.assertEqual(len(config.get_window_patterns()), 2)


if __name__ == "__main__":
    unittest.main()
