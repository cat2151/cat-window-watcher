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


if __name__ == "__main__":
    unittest.main()
