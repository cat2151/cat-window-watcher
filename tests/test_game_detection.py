#!/usr/bin/env python3
"""Tests for game playing detection functionality."""

import tempfile
import unittest
from pathlib import Path

try:
    from src.config import Config
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config


class TestGameDetection(unittest.TestCase):
    """Test cases for game playing detection configuration."""

    def test_game_detection_default_disabled(self):
        """Test that game detection is disabled by default."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            config = Config(config_path)
            game_detection = config.get_game_playing_detection()

            self.assertFalse(game_detection["enabled"])
            self.assertEqual(game_detection["process_names"], [])
            self.assertEqual(game_detection["check_interval_seconds"], 60)
        finally:
            Path(config_path).unlink()

    def test_game_detection_enabled_with_process_names(self):
        """Test enabling game detection with process names."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = ["StreetFighter6.exe", "SF6.exe"]
check_interval_seconds = 60

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            config = Config(config_path)
            game_detection = config.get_game_playing_detection()

            self.assertTrue(game_detection["enabled"])
            self.assertEqual(game_detection["process_names"], ["StreetFighter6.exe", "SF6.exe"])
            self.assertEqual(game_detection["check_interval_seconds"], 60)
        finally:
            Path(config_path).unlink()

    def test_game_detection_custom_interval(self):
        """Test game detection with custom check interval."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = ["game.exe"]
check_interval_seconds = 120

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            config = Config(config_path)
            game_detection = config.get_game_playing_detection()

            self.assertTrue(game_detection["enabled"])
            self.assertEqual(game_detection["process_names"], ["game.exe"])
            self.assertEqual(game_detection["check_interval_seconds"], 120)
        finally:
            Path(config_path).unlink()

    def test_game_detection_empty_process_names(self):
        """Test game detection with empty process names list."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = []
check_interval_seconds = 60

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            config = Config(config_path)
            game_detection = config.get_game_playing_detection()

            self.assertTrue(game_detection["enabled"])
            self.assertEqual(game_detection["process_names"], [])
            self.assertEqual(game_detection["check_interval_seconds"], 60)
        finally:
            Path(config_path).unlink()

    def test_game_detection_invalid_process_names_type(self):
        """Test that invalid process_names type raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = "not_a_list"
check_interval_seconds = 60

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            with self.assertRaises(SystemExit):
                Config(config_path)
        finally:
            Path(config_path).unlink()

    def test_game_detection_invalid_interval_type(self):
        """Test that invalid check_interval_seconds type raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = ["game.exe"]
check_interval_seconds = "sixty"

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            with self.assertRaises(SystemExit):
                Config(config_path)
        finally:
            Path(config_path).unlink()

    def test_game_detection_negative_interval(self):
        """Test that negative check_interval_seconds raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = ["game.exe"]
check_interval_seconds = -1

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            with self.assertRaises(SystemExit):
                Config(config_path)
        finally:
            Path(config_path).unlink()

    def test_game_detection_zero_interval(self):
        """Test that zero check_interval_seconds raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = ["game.exe"]
check_interval_seconds = 0

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            with self.assertRaises(SystemExit):
                Config(config_path)
        finally:
            Path(config_path).unlink()

    def test_game_detection_process_names_with_non_string(self):
        """Test that process_names with non-string elements raises error."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(
                """
[game_playing_detection]
enabled = true
process_names = ["game.exe", 123, "another.exe"]
check_interval_seconds = 60

[[window_patterns]]
description = "Test"
regex = "test"
score = 1
"""
            )
            f.flush()
            config_path = f.name

        try:
            with self.assertRaises(SystemExit):
                Config(config_path)
        finally:
            Path(config_path).unlink()


if __name__ == "__main__":
    unittest.main()
