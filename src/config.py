#!/usr/bin/env python3
"""Configuration module for cat-window-watcher."""

import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class Config:
    """Configuration manager for window watcher."""

    def __init__(self, config_path: str = "config.toml"):
        """Initialize configuration.

        Args:
            config_path: Path to TOML configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
        """
        self.config_path = Path(config_path)
        self.window_patterns = []
        self.default_score = -1
        self._last_modified = None
        self.load_config()

    def load_config(self):
        """Load configuration from TOML file.

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
        """
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomllib.load(f)

            # Load default_score (score applied when no pattern matches)
            self.default_score = config_data.get("default_score", -1)

            # Load window patterns with their score values
            self.window_patterns = []
            for pattern in config_data.get("window_patterns", []):
                self.window_patterns.append(
                    {
                        "regex": pattern.get("regex", ""),
                        "score": pattern.get("score", 0),
                        "description": pattern.get("description", ""),
                    }
                )

            # Update last modified timestamp
            self._last_modified = self.config_path.stat().st_mtime

        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_path}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to load configuration: {e}")
            sys.exit(1)

    def is_modified(self):
        """Check if configuration file has been modified.

        Returns:
            bool: True if file has been modified since last load, False otherwise
        """
        try:
            current_mtime = self.config_path.stat().st_mtime
            return current_mtime != self._last_modified
        except Exception:
            return False

    def reload_if_modified(self):
        """Reload configuration if the file has been modified.

        Returns:
            bool: True if configuration was reloaded, False otherwise
        """
        if self.is_modified():
            try:
                self.load_config()
                print(f"Configuration reloaded from '{self.config_path}'")
                return True
            except Exception as e:
                print(f"Warning: Failed to reload configuration: {e}")
                return False
        return False

    def get_window_patterns(self):
        """Get list of window patterns.

        Returns:
            list: List of pattern dictionaries with regex, score, and description
        """
        return self.window_patterns

    def get_default_score(self):
        """Get default score for non-matching windows.

        Returns:
            int: Default score value
        """
        return self.default_score
