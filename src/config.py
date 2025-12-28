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
        self.apply_default_score_mode = True
        self.always_on_top = False
        self.hide_on_mouse_proximity = False
        self.proximity_distance = 50
        self.mild_penalty_mode = False
        self.mild_penalty_start_hour = 22
        self.mild_penalty_end_hour = 23
        self.score_up_color = "#ffffff"
        self.score_down_color = "#ff0000"
        self._last_modified = None
        self.load_config()

    def load_config(self, exit_on_error=True):
        """Load configuration from TOML file.

        Args:
            exit_on_error: If True, exit on error. If False, raise exception.

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
            Exception: If other errors occur during loading
        """
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomllib.load(f)

            # Load default_score (score applied when no pattern matches)
            default_score = config_data.get("default_score", -1)

            # Load apply_default_score_mode setting (whether to apply default score)
            apply_default_score_mode = config_data.get("apply_default_score_mode", True)
            if not isinstance(apply_default_score_mode, bool):
                raise ValueError(
                    f"Invalid 'apply_default_score_mode' value: {apply_default_score_mode!r}. Must be a boolean."
                )

            # Load always_on_top setting (whether window should stay on top)
            always_on_top = config_data.get("always_on_top", False)

            # Load hide_on_mouse_proximity setting (hide window when mouse is near)
            hide_on_mouse_proximity = config_data.get("hide_on_mouse_proximity", False)

            # Load proximity_distance setting (distance in pixels)
            # Ensure it is a non-negative integer; raise error if invalid
            proximity_distance = config_data.get("proximity_distance", 50)
            if not isinstance(proximity_distance, int) or proximity_distance < 0:
                raise ValueError(
                    f"Invalid 'proximity_distance' value: {proximity_distance!r}. Must be a non-negative integer."
                )

            # Load mild_penalty_mode setting (whether to apply mild penalty during specified hours)
            mild_penalty_mode = config_data.get("mild_penalty_mode", False)
            if not isinstance(mild_penalty_mode, bool):
                raise ValueError(f"Invalid 'mild_penalty_mode' value: {mild_penalty_mode!r}. Must be a boolean.")

            # Load mild_penalty_start_hour setting (start hour for mild penalty, default: 22)
            mild_penalty_start_hour = config_data.get("mild_penalty_start_hour", 22)
            if not isinstance(mild_penalty_start_hour, int) or not (0 <= mild_penalty_start_hour <= 23):
                raise ValueError(
                    f"Invalid 'mild_penalty_start_hour' value: {mild_penalty_start_hour!r}. Must be an integer between 0 and 23."
                )

            # Load mild_penalty_end_hour setting (end hour for mild penalty, default: 23)
            mild_penalty_end_hour = config_data.get("mild_penalty_end_hour", 23)
            if not isinstance(mild_penalty_end_hour, int) or not (0 <= mild_penalty_end_hour <= 23):
                raise ValueError(
                    f"Invalid 'mild_penalty_end_hour' value: {mild_penalty_end_hour!r}. Must be an integer between 0 and 23."
                )

            # Load score color settings (font color for score increase/decrease)
            score_up_color = config_data.get("score_up_color", "#ffffff")
            score_down_color = config_data.get("score_down_color", "#ff0000")

            # Validate color format (basic validation for hex color)
            if not isinstance(score_up_color, str) or not score_up_color.startswith("#"):
                raise ValueError(
                    f"Invalid 'score_up_color' value: {score_up_color!r}. Must be a hex color string (e.g., '#ffffff')."
                )
            if not isinstance(score_down_color, str) or not score_down_color.startswith("#"):
                raise ValueError(
                    f"Invalid 'score_down_color' value: {score_down_color!r}. Must be a hex color string (e.g., '#ff0000')."
                )

            # Load window patterns with their score values
            window_patterns = []
            for pattern in config_data.get("window_patterns", []):
                window_patterns.append(
                    {
                        "regex": pattern.get("regex", ""),
                        "score": pattern.get("score", 0),
                        "description": pattern.get("description", ""),
                    }
                )

            # Only update instance attributes after successful parsing
            self.default_score = default_score
            self.apply_default_score_mode = apply_default_score_mode
            self.always_on_top = always_on_top
            self.hide_on_mouse_proximity = hide_on_mouse_proximity
            self.proximity_distance = proximity_distance
            self.mild_penalty_mode = mild_penalty_mode
            self.mild_penalty_start_hour = mild_penalty_start_hour
            self.mild_penalty_end_hour = mild_penalty_end_hour
            self.score_up_color = score_up_color
            self.score_down_color = score_down_color
            self.window_patterns = window_patterns

            # Update last modified timestamp after successful load
            self._last_modified = self.config_path.stat().st_mtime

        except FileNotFoundError:
            if exit_on_error:
                print(f"Error: Configuration file '{self.config_path}' not found.")
                sys.exit(1)
            else:
                raise
        except Exception as e:
            if exit_on_error:
                print(f"Error: Failed to load configuration: {e}")
                sys.exit(1)
            else:
                raise

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
                self.load_config(exit_on_error=False)
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

    def get_apply_default_score_mode(self):
        """Get apply_default_score_mode setting.

        Returns:
            bool: True if default score should be applied when no pattern matches, False otherwise
        """
        return self.apply_default_score_mode

    def get_always_on_top(self):
        """Get always_on_top setting.

        Returns:
            bool: True if window should stay on top, False otherwise
        """
        return self.always_on_top

    def get_hide_on_mouse_proximity(self):
        """Get hide_on_mouse_proximity setting.

        Returns:
            bool: True if window should hide when mouse is near, False otherwise
        """
        return self.hide_on_mouse_proximity

    def get_proximity_distance(self):
        """Get proximity_distance setting.

        Returns:
            int: Distance in pixels to trigger proximity behavior
        """
        return self.proximity_distance

    def get_mild_penalty_mode(self):
        """Get mild_penalty_mode setting.

        Returns:
            bool: True if mild penalty mode is enabled, False otherwise
        """
        return self.mild_penalty_mode

    def get_mild_penalty_start_hour(self):
        """Get mild_penalty_start_hour setting.

        Returns:
            int: Start hour for mild penalty mode (0-23)
        """
        return self.mild_penalty_start_hour

    def get_mild_penalty_end_hour(self):
        """Get mild_penalty_end_hour setting.

        Returns:
            int: End hour for mild penalty mode (0-23)
        """
        return self.mild_penalty_end_hour

    def get_score_up_color(self):
        """Get score_up_color setting.

        Returns:
            str: Hex color string for score increase (e.g., '#ffffff')
        """
        return self.score_up_color

    def get_score_down_color(self):
        """Get score_down_color setting.

        Returns:
            str: Hex color string for score decrease (e.g., '#ff0000')
        """
        return self.score_down_color
