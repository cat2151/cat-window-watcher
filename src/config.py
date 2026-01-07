#!/usr/bin/env python3
"""Configuration module for cat-window-watcher."""

import sys
from datetime import datetime
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

# ANSI color codes for console output
ANSI_GREEN = "\033[32m"
ANSI_RESET = "\033[0m"


class Config:
    """Configuration manager for window watcher."""

    def __init__(self, config_path: str = "config.toml", verbose: bool = False):
        """Initialize configuration.

        Args:
            config_path: Path to TOML configuration file
            verbose: Deprecated parameter. The verbose setting is now controlled
                     via the 'verbose' option in the TOML configuration file.
                     This parameter is ignored and will be removed in a future version.
                     Use `verbose = true/false` in your config.toml instead.

        Raises:
            FileNotFoundError: If config file doesn't exist
            tomllib.TOMLDecodeError: If config file is invalid
        """
        self.config_path = Path(config_path)
        self.verbose = False  # Will be overridden by TOML config
        self.window_patterns = []
        self.default_score = -1
        self.apply_default_score_mode = True
        self.self_window_score = 0
        self.always_on_top = True
        self.hide_on_mouse_proximity = True
        self.proximity_distance = 50
        self.always_on_top_while_score_decreasing = True
        self.mild_penalty_mode = False
        self.mild_penalty_start_hour = 22
        self.mild_penalty_end_hour = 23
        self.score_up_color = "#ffffff"
        self.score_down_color = "#ff0000"
        self.reset_score_every_30_minutes = True
        self.fade_window_on_flow_mode_enabled = False
        self.flow_mode_delay_seconds = 10
        self.flow_mode_fade_rate_percent_per_second = 1
        self.default_transparency = 1.0
        self.window_x = None
        self.window_y = None
        self._last_modified = None
        self.load_config()

    @staticmethod
    def _validate_hex_color(color_value, color_name):
        """Validate hex color format.

        Args:
            color_value: Color value to validate
            color_name: Name of the color setting (for error messages)

        Raises:
            ValueError: If color format is invalid
        """
        if not isinstance(color_value, str):
            raise ValueError(
                f"Invalid '{color_name}' value: {color_value!r}. Must be a hex color string (e.g., '#ffffff')."
            )
        if not color_value.startswith("#") or len(color_value) != 7:
            raise ValueError(
                f"Invalid '{color_name}' value: {color_value!r}. Must be a 7-character hex color string (e.g., '#ffffff')."
            )
        try:
            # Validate hex digits after '#'
            int(color_value[1:], 16)
        except ValueError:
            raise ValueError(
                f"Invalid '{color_name}' value: {color_value!r}. Must contain valid hex digits after '#' (0-9, a-f)."
            ) from None

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

            # Load verbose mode setting (whether to print configuration on load)
            verbose = config_data.get("verbose", False)
            if not isinstance(verbose, bool):
                raise ValueError(f"Invalid 'verbose' value: {verbose!r}. Must be a boolean.")

            # Load default_score (score applied when no pattern matches)
            default_score = config_data.get("default_score", -1)

            # Load apply_default_score_mode setting (whether to apply default score)
            apply_default_score_mode = config_data.get("apply_default_score_mode", True)
            if not isinstance(apply_default_score_mode, bool):
                raise ValueError(
                    f"Invalid 'apply_default_score_mode' value: {apply_default_score_mode!r}. Must be a boolean."
                )

            # Load self_window_score (score applied when app's own window is active)
            self_window_score = config_data.get("self_window_score", 0)
            if not isinstance(self_window_score, int):
                raise ValueError(f"Invalid 'self_window_score' value: {self_window_score!r}. Must be an integer.")

            # Load always_on_top setting (whether window should stay on top)
            always_on_top = config_data.get("always_on_top", True)

            # Load hide_on_mouse_proximity setting (hide window when mouse is near)
            hide_on_mouse_proximity = config_data.get("hide_on_mouse_proximity", True)

            # Load proximity_distance setting (distance in pixels)
            # Ensure it is a non-negative integer; raise error if invalid
            proximity_distance = config_data.get("proximity_distance", 50)
            if not isinstance(proximity_distance, int) or proximity_distance < 0:
                raise ValueError(
                    f"Invalid 'proximity_distance' value: {proximity_distance!r}. Must be a non-negative integer."
                )

            # Load always_on_top_while_score_decreasing setting
            always_on_top_while_score_decreasing = config_data.get("always_on_top_while_score_decreasing", True)
            if not isinstance(always_on_top_while_score_decreasing, bool):
                raise ValueError(
                    f"Invalid 'always_on_top_while_score_decreasing' value: {always_on_top_while_score_decreasing!r}. Must be a boolean."
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

            # Validate color format
            self._validate_hex_color(score_up_color, "score_up_color")
            self._validate_hex_color(score_down_color, "score_down_color")

            # Load reset_score_every_30_minutes setting (reset score at :00 and :30 of each hour)
            reset_score_every_30_minutes = config_data.get("reset_score_every_30_minutes", True)
            if not isinstance(reset_score_every_30_minutes, bool):
                raise ValueError(
                    f"Invalid 'reset_score_every_30_minutes' value: {reset_score_every_30_minutes!r}. Must be a boolean."
                )

            # Load fade_window_on_flow_mode_enabled setting (fade window transparency when in flow state)
            fade_window_on_flow_mode_enabled = config_data.get("fade_window_on_flow_mode_enabled", False)
            if not isinstance(fade_window_on_flow_mode_enabled, bool):
                raise ValueError(
                    f"Invalid 'fade_window_on_flow_mode_enabled' value: {fade_window_on_flow_mode_enabled!r}. Must be a boolean."
                )

            # Load flow_mode_delay_seconds setting (delay before starting fade in flow mode)
            flow_mode_delay_seconds = config_data.get("flow_mode_delay_seconds", 10)
            if not isinstance(flow_mode_delay_seconds, int) or flow_mode_delay_seconds < 0:
                raise ValueError(
                    f"Invalid 'flow_mode_delay_seconds' value: {flow_mode_delay_seconds!r}. Must be a non-negative integer."
                )

            # Load flow_mode_fade_rate_percent_per_second setting (fade rate in percent per second)
            flow_mode_fade_rate_percent_per_second = config_data.get("flow_mode_fade_rate_percent_per_second", 1)
            if (
                not isinstance(flow_mode_fade_rate_percent_per_second, int)
                or flow_mode_fade_rate_percent_per_second <= 0
                or flow_mode_fade_rate_percent_per_second > 100
            ):
                raise ValueError(
                    f"Invalid 'flow_mode_fade_rate_percent_per_second' value: {flow_mode_fade_rate_percent_per_second!r}. Must be an integer between 1 and 100."
                )

            # Load window_x setting (initial x coordinate for window position)
            window_x = config_data.get("window_x", None)
            if window_x is not None and not isinstance(window_x, int):
                raise ValueError(f"Invalid 'window_x' value: {window_x!r}. Must be an integer or null.")

            # Load window_y setting (initial y coordinate for window position)
            window_y = config_data.get("window_y", None)
            if window_y is not None and not isinstance(window_y, int):
                raise ValueError(f"Invalid 'window_y' value: {window_y!r}. Must be an integer or null.")

            # Load default_transparency setting (default window transparency/opacity, 0.0-1.0)
            default_transparency = config_data.get("default_transparency", 1.0)
            if not isinstance(default_transparency, (int, float)):
                raise ValueError(
                    f"Invalid 'default_transparency' value: {default_transparency!r}. Must be a number (int or float)."
                )
            if not (0.0 <= default_transparency <= 1.0):
                raise ValueError(
                    f"Invalid 'default_transparency' value: {default_transparency!r}. Must be between 0.0 and 1.0."
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
            self.verbose = verbose
            self.default_score = default_score
            self.apply_default_score_mode = apply_default_score_mode
            self.self_window_score = self_window_score
            self.always_on_top = always_on_top
            self.hide_on_mouse_proximity = hide_on_mouse_proximity
            self.proximity_distance = proximity_distance
            self.always_on_top_while_score_decreasing = always_on_top_while_score_decreasing
            self.mild_penalty_mode = mild_penalty_mode
            self.mild_penalty_start_hour = mild_penalty_start_hour
            self.mild_penalty_end_hour = mild_penalty_end_hour
            self.score_up_color = score_up_color
            self.score_down_color = score_down_color
            self.reset_score_every_30_minutes = reset_score_every_30_minutes
            self.fade_window_on_flow_mode_enabled = fade_window_on_flow_mode_enabled
            self.flow_mode_delay_seconds = flow_mode_delay_seconds
            self.flow_mode_fade_rate_percent_per_second = flow_mode_fade_rate_percent_per_second
            self.default_transparency = default_transparency
            self.window_x = window_x
            self.window_y = window_y
            self.window_patterns = window_patterns

            # Update last modified timestamp after successful load
            self._last_modified = self.config_path.stat().st_mtime

            # Print configuration values to console if verbose mode is enabled
            if self.verbose:
                self.print_config()

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
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{ANSI_GREEN}Configuration reloaded from '{self.config_path}' at {timestamp}{ANSI_RESET}")
                self.load_config(exit_on_error=False)
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

    def get_self_window_score(self):
        """Get self_window_score setting.

        Returns:
            int: Score to apply when app's own window is active
        """
        return self.self_window_score

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

    def get_always_on_top_while_score_decreasing(self):
        """Get always_on_top_while_score_decreasing setting.

        Returns:
            bool: True if window should stay on top while score decreases, False otherwise
        """
        return self.always_on_top_while_score_decreasing

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

    def get_reset_score_every_30_minutes(self):
        """Get reset_score_every_30_minutes setting.

        Returns:
            bool: True if score should reset every 30 minutes, False otherwise
        """
        return self.reset_score_every_30_minutes

    def get_fade_window_on_flow_mode_enabled(self):
        """Get fade_window_on_flow_mode_enabled setting.

        Returns:
            bool: True if window should fade when in flow mode, False otherwise
        """
        return self.fade_window_on_flow_mode_enabled

    def get_flow_mode_delay_seconds(self):
        """Get flow_mode_delay_seconds setting.

        Returns:
            int: Delay in seconds before starting fade in flow mode
        """
        return self.flow_mode_delay_seconds

    def get_flow_mode_fade_rate_percent_per_second(self):
        """Get flow_mode_fade_rate_percent_per_second setting.

        Returns:
            int: Fade rate in percent per second (1-100)
        """
        return self.flow_mode_fade_rate_percent_per_second

    def get_default_transparency(self):
        """Get default_transparency setting.

        Returns:
            float: Default window transparency (0.0 = fully transparent, 1.0 = fully opaque)
        """
        return self.default_transparency

    def get_window_x(self):
        """Get window_x setting.

        Returns:
            int or None: Initial x coordinate for window position, or None for default
        """
        return self.window_x

    def get_window_y(self):
        """Get window_y setting.

        Returns:
            int or None: Initial y coordinate for window position, or None for default
        """
        return self.window_y

    def get_verbose(self):
        """Get verbose mode setting.

        Returns:
            bool: True if verbose mode is enabled, False otherwise
        """
        return self.verbose

    def print_config(self, context: str = ""):
        """Print all configuration values to console.

        Args:
            context: Optional context string to add to header (e.g., "リロード後")

        This method outputs all settings including default values,
        helping users understand the current configuration state.
        """
        print("=" * 60)
        header = "現在の設定値 (Current Configuration)"
        if context:
            header += f" {context}"
        print(header)
        print("=" * 60)
        print(f"設定ファイル (Config file): {self.config_path}")
        print()
        print("--- スコア設定 (Score Settings) ---")
        print(f"default_score: {self.default_score}")
        print(f"apply_default_score_mode: {self.apply_default_score_mode}")
        print(f"self_window_score: {self.self_window_score}")
        print()
        print("--- ウィンドウ表示設定 (Window Display Settings) ---")
        print(f"always_on_top: {self.always_on_top}")
        print(f"hide_on_mouse_proximity: {self.hide_on_mouse_proximity}")
        print(f"proximity_distance: {self.proximity_distance}")
        print(f"always_on_top_while_score_decreasing: {self.always_on_top_while_score_decreasing}")
        print(f"default_transparency: {self.default_transparency}")
        print(f"window_x: {self.window_x}")
        print(f"window_y: {self.window_y}")
        print()
        print("--- スコア表示設定 (Score Display Settings) ---")
        print(f"score_up_color: {self.score_up_color}")
        print(f"score_down_color: {self.score_down_color}")
        print()
        print("--- ペナルティモード設定 (Penalty Mode Settings) ---")
        print(f"mild_penalty_mode: {self.mild_penalty_mode}")
        print(f"mild_penalty_start_hour: {self.mild_penalty_start_hour}")
        print(f"mild_penalty_end_hour: {self.mild_penalty_end_hour}")
        print()
        print("--- 時間管理設定 (Time Management Settings) ---")
        print(f"reset_score_every_30_minutes: {self.reset_score_every_30_minutes}")
        print()
        print("--- フローモード設定 (Flow Mode Settings) ---")
        print(f"fade_window_on_flow_mode_enabled: {self.fade_window_on_flow_mode_enabled}")
        print(f"flow_mode_delay_seconds: {self.flow_mode_delay_seconds}")
        print(f"flow_mode_fade_rate_percent_per_second: {self.flow_mode_fade_rate_percent_per_second}")
        print()
        print("--- ウィンドウパターン (Window Patterns) ---")
        if self.window_patterns:
            for i, pattern in enumerate(self.window_patterns, 1):
                print(f"  [{i}] {pattern['description'] or '(no description)'}")
                print(f"      regex: {pattern['regex']}")
                print(f"      score: {pattern['score']}")
        else:
            print("  (パターンが定義されていません / No patterns defined)")
        print("=" * 60)
