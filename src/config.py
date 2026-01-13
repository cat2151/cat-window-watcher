#!/usr/bin/env python3
"""Configuration module for cat-window-watcher."""

from datetime import datetime
from pathlib import Path

try:
    from .config_loader import ConfigLoader
except ImportError:
    from config_loader import ConfigLoader

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
            Exception: If config file is invalid
        """
        self.config_path = Path(config_path)
        self._loader = ConfigLoader(config_path)
        self._last_modified = None

        # Initialize default values
        self.verbose = False
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
        self.fade_window_on_flow_mode_enabled = True
        self.flow_mode_delay_seconds = 3
        self.flow_mode_fade_rate_percent_per_second = 20
        self.default_transparency = 1.0
        self.window_x = None
        self.window_y = None

        # Load configuration and print initial load message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ANSI_GREEN}Configuration loaded from '{self.config_path}' at {timestamp}{ANSI_RESET}")
        self.load_config()

    def load_config(self, exit_on_error=True):
        """Load configuration from TOML file.

        Args:
            exit_on_error: If True, exit on error. If False, raise exception.

        Raises:
            FileNotFoundError: If config file doesn't exist
            Exception: If config file is invalid or validation fails
        """
        settings = self._loader.load(exit_on_error=exit_on_error)

        # Update instance attributes with loaded settings
        self.verbose = settings["verbose"]
        self.default_score = settings["default_score"]
        self.apply_default_score_mode = settings["apply_default_score_mode"]
        self.self_window_score = settings["self_window_score"]
        self.always_on_top = settings["always_on_top"]
        self.hide_on_mouse_proximity = settings["hide_on_mouse_proximity"]
        self.proximity_distance = settings["proximity_distance"]
        self.always_on_top_while_score_decreasing = settings["always_on_top_while_score_decreasing"]
        self.mild_penalty_mode = settings["mild_penalty_mode"]
        self.mild_penalty_start_hour = settings["mild_penalty_start_hour"]
        self.mild_penalty_end_hour = settings["mild_penalty_end_hour"]
        self.score_up_color = settings["score_up_color"]
        self.score_down_color = settings["score_down_color"]
        self.reset_score_every_30_minutes = settings["reset_score_every_30_minutes"]
        self.fade_window_on_flow_mode_enabled = settings["fade_window_on_flow_mode_enabled"]
        self.flow_mode_delay_seconds = settings["flow_mode_delay_seconds"]
        self.flow_mode_fade_rate_percent_per_second = settings["flow_mode_fade_rate_percent_per_second"]
        self.default_transparency = settings["default_transparency"]
        self.window_x = settings["window_x"]
        self.window_y = settings["window_y"]
        self.window_patterns = settings["window_patterns"]
        self._last_modified = settings["_last_modified"]

        # Print configuration values to console if verbose mode is enabled
        if self.verbose:
            self.print_config()

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
