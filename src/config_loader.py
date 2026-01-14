#!/usr/bin/env python3
"""Configuration loading module for cat-window-watcher."""

import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

try:
    from .config_validator import ConfigValidator
except ImportError:
    from config_validator import ConfigValidator


class ConfigLoader:
    """Loader for TOML configuration files."""

    def __init__(self, config_path):
        """Initialize configuration loader.

        Args:
            config_path: Path to TOML configuration file
        """
        self.config_path = Path(config_path)
        self.validator = ConfigValidator()

    def load(self, exit_on_error=True):
        """Load configuration from TOML file.

        Args:
            exit_on_error: If True, exit on error. If False, raise exception.

        Returns:
            dict: Configuration dictionary with all settings

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
            ValueError: If configuration values are invalid
        """
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomllib.load(f)

            # Parse and validate all settings
            settings = self._parse_settings(config_data)

            # Update last modified timestamp
            settings["_last_modified"] = self.config_path.stat().st_mtime

            return settings

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

    def _parse_settings(self, config_data):
        """Parse and validate configuration settings.

        Args:
            config_data: Raw configuration data from TOML

        Returns:
            dict: Validated configuration settings
        """
        settings = {}

        # Verbose mode
        verbose = config_data.get("verbose", False)
        self.validator.validate_boolean(verbose, "verbose")
        settings["verbose"] = verbose

        # Debug screensaver detection
        debug_screensaver_detection = config_data.get("debug_screensaver_detection", False)
        self.validator.validate_boolean(debug_screensaver_detection, "debug_screensaver_detection")
        settings["debug_screensaver_detection"] = debug_screensaver_detection

        # Default score
        default_score = config_data.get("default_score", -1)
        self.validator.validate_integer(default_score, "default_score")
        settings["default_score"] = default_score

        # Apply default score mode
        apply_default_score_mode = config_data.get("apply_default_score_mode", True)
        self.validator.validate_boolean(apply_default_score_mode, "apply_default_score_mode")
        settings["apply_default_score_mode"] = apply_default_score_mode

        # Self window score
        self_window_score = config_data.get("self_window_score", 0)
        self.validator.validate_integer(self_window_score, "self_window_score")
        settings["self_window_score"] = self_window_score

        # Always on top
        always_on_top = config_data.get("always_on_top", True)
        self.validator.validate_boolean(always_on_top, "always_on_top")
        settings["always_on_top"] = always_on_top

        # Hide on mouse proximity
        hide_on_mouse_proximity = config_data.get("hide_on_mouse_proximity", True)
        self.validator.validate_boolean(hide_on_mouse_proximity, "hide_on_mouse_proximity")
        settings["hide_on_mouse_proximity"] = hide_on_mouse_proximity

        # Proximity distance
        proximity_distance = config_data.get("proximity_distance", 50)
        self.validator.validate_non_negative_integer(proximity_distance, "proximity_distance")
        settings["proximity_distance"] = proximity_distance

        # Always on top while score decreasing
        always_on_top_while_score_decreasing = config_data.get("always_on_top_while_score_decreasing", True)
        self.validator.validate_boolean(always_on_top_while_score_decreasing, "always_on_top_while_score_decreasing")
        settings["always_on_top_while_score_decreasing"] = always_on_top_while_score_decreasing

        # Mild penalty mode
        mild_penalty_mode = config_data.get("mild_penalty_mode", False)
        self.validator.validate_boolean(mild_penalty_mode, "mild_penalty_mode")
        settings["mild_penalty_mode"] = mild_penalty_mode

        # Mild penalty start hour
        mild_penalty_start_hour = config_data.get("mild_penalty_start_hour", 22)
        self.validator.validate_hour(mild_penalty_start_hour, "mild_penalty_start_hour")
        settings["mild_penalty_start_hour"] = mild_penalty_start_hour

        # Mild penalty end hour
        mild_penalty_end_hour = config_data.get("mild_penalty_end_hour", 23)
        self.validator.validate_hour(mild_penalty_end_hour, "mild_penalty_end_hour")
        settings["mild_penalty_end_hour"] = mild_penalty_end_hour

        # Score colors
        score_up_color = config_data.get("score_up_color", "#ffffff")
        score_down_color = config_data.get("score_down_color", "#ff0000")
        self.validator.validate_hex_color(score_up_color, "score_up_color")
        self.validator.validate_hex_color(score_down_color, "score_down_color")
        settings["score_up_color"] = score_up_color
        settings["score_down_color"] = score_down_color

        # Reset score every 30 minutes
        reset_score_every_30_minutes = config_data.get("reset_score_every_30_minutes", True)
        self.validator.validate_boolean(reset_score_every_30_minutes, "reset_score_every_30_minutes")
        settings["reset_score_every_30_minutes"] = reset_score_every_30_minutes

        # Fade window on flow mode enabled
        fade_window_on_flow_mode_enabled = config_data.get("fade_window_on_flow_mode_enabled", True)
        self.validator.validate_boolean(fade_window_on_flow_mode_enabled, "fade_window_on_flow_mode_enabled")
        settings["fade_window_on_flow_mode_enabled"] = fade_window_on_flow_mode_enabled

        # Flow mode delay seconds
        flow_mode_delay_seconds = config_data.get("flow_mode_delay_seconds", 3)
        self.validator.validate_non_negative_integer(flow_mode_delay_seconds, "flow_mode_delay_seconds")
        settings["flow_mode_delay_seconds"] = flow_mode_delay_seconds

        # Flow mode fade rate
        flow_mode_fade_rate_percent_per_second = config_data.get("flow_mode_fade_rate_percent_per_second", 20)
        self.validator.validate_percentage(
            flow_mode_fade_rate_percent_per_second, "flow_mode_fade_rate_percent_per_second"
        )
        settings["flow_mode_fade_rate_percent_per_second"] = flow_mode_fade_rate_percent_per_second

        # Window position
        window_x = config_data.get("window_x", None)
        window_y = config_data.get("window_y", None)
        self.validator.validate_optional_integer(window_x, "window_x")
        self.validator.validate_optional_integer(window_y, "window_y")
        settings["window_x"] = window_x
        settings["window_y"] = window_y

        # Default transparency
        default_transparency = config_data.get("default_transparency", 1.0)
        self.validator.validate_transparency(default_transparency, "default_transparency")
        settings["default_transparency"] = default_transparency

        # Window patterns
        window_patterns = []
        for pattern in config_data.get("window_patterns", []):
            window_patterns.append(
                {
                    "regex": pattern.get("regex", ""),
                    "score": pattern.get("score", 1),
                    "description": pattern.get("description", ""),
                }
            )
        settings["window_patterns"] = window_patterns

        return settings
