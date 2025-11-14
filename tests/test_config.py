#!/usr/bin/env python3
"""Tests for config module."""

import tempfile
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
        """Test default_score defaults to 0 when not specified."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        self.assertEqual(config.get_default_score(), 0)

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


if __name__ == "__main__":
    unittest.main()
