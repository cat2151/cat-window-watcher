#!/usr/bin/env python3
"""Shared mock classes for GUI tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

_StatusFormatter = None
MAX_WINDOW_TITLE_LENGTH = None

try:
    from src.config import Config  # noqa: F401
    from src.score_tracker import ScoreTracker  # noqa: F401
    from src.status_formatter import MAX_WINDOW_TITLE_LENGTH
    from src.status_formatter import StatusFormatter as _StatusFormatter
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config  # noqa: F401
    from score_tracker import ScoreTracker  # noqa: F401

    try:
        from status_formatter import MAX_WINDOW_TITLE_LENGTH
        from status_formatter import StatusFormatter as _StatusFormatter
    except ImportError:
        pass

# If status_formatter is not available, provide a standalone fallback constant.
# This should not occur in normal environments since status_formatter has no heavy dependencies.
if MAX_WINDOW_TITLE_LENGTH is None:
    MAX_WINDOW_TITLE_LENGTH = 40


def get_status_text(matched_pattern, window_title, default_score, elapsed_seconds=0, flow_mode_seconds=0):
    """Thin wrapper around StatusFormatter.format_status_text for GUI tests.

    Tests use this wrapper so they validate the production logic in StatusFormatter,
    not a duplicated fallback. Falls back to a local implementation only when
    status_formatter cannot be imported (should not occur in normal environments).
    """
    if _StatusFormatter is not None:
        return _StatusFormatter.format_status_text(
            matched_pattern, window_title, default_score, elapsed_seconds, flow_mode_seconds
        )

    # Emergency fallback (status_formatter unavailable)
    if flow_mode_seconds > 0:
        elapsed_text = f" [フロー: {flow_mode_seconds}秒]"
    elif elapsed_seconds > 0:
        elapsed_text = f" [{elapsed_seconds}秒]"
    else:
        elapsed_text = ""

    if matched_pattern:
        description = matched_pattern.get("description", "")
        score_delta = matched_pattern.get("score", 0)
        score_sign = "+" if score_delta >= 0 else ""
        return f"{description} ({score_sign}{score_delta}){elapsed_text}"
    else:
        display_title = (
            window_title[:MAX_WINDOW_TITLE_LENGTH] + "..."
            if len(window_title) > MAX_WINDOW_TITLE_LENGTH
            else window_title
        )
        if default_score != 0:
            score_sign = "+" if default_score >= 0 else ""
            score_text = f"({score_sign}{default_score})"
            return (
                f"No match: {display_title} {score_text}{elapsed_text}"
                if display_title
                else f"No match {score_text}{elapsed_text}"
            )
        else:
            return f"{display_title}{elapsed_text}" if display_title else f"Watching...{elapsed_text}"


class MockScoreDisplay:
    """Mock ScoreDisplay class for testing proximity detection logic."""

    def __init__(self, score_tracker, config):
        self.score_tracker = score_tracker
        self.config = config
        self._mouse_in_proximity = False
        self._previous_always_on_top = None
        self._current_window_title = ""
        self._previous_window_title = ""
        self.root = MagicMock()

    def _apply_always_on_top(self):
        """Apply always_on_top setting to the window."""
        current_always_on_top = self.config.get_always_on_top()

        # Only update if the setting has changed
        if current_always_on_top != self._previous_always_on_top:
            self.root.attributes("-topmost", current_always_on_top)
            self._previous_always_on_top = current_always_on_top

    def _is_mouse_in_proximity(self):
        """Check if mouse is within proximity distance of the window."""
        # Get mouse position relative to screen
        mouse_x = self.root.winfo_pointerx()
        mouse_y = self.root.winfo_pointery()

        # Get window position and dimensions
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Get proximity distance from config
        proximity_distance = self.config.get_proximity_distance()

        # Calculate if mouse is within proximity distance
        # Check if mouse is within the expanded bounding box
        in_proximity = (
            mouse_x >= window_x - proximity_distance
            and mouse_x <= window_x + window_width + proximity_distance
            and mouse_y >= window_y - proximity_distance
            and mouse_y <= window_y + window_height + proximity_distance
        )

        return in_proximity

    def _update_proximity_based_topmost(self):
        """Update window topmost state based on mouse proximity."""
        # Only apply proximity-based behavior if both settings are enabled
        if not self.config.get_always_on_top() or not self.config.get_hide_on_mouse_proximity():
            return

        # Check if mouse is in proximity
        mouse_in_proximity = self._is_mouse_in_proximity()

        # Update topmost state if proximity state changed
        if mouse_in_proximity != self._mouse_in_proximity:
            self._mouse_in_proximity = mouse_in_proximity

            # If mouse is in proximity, remove topmost (send to back)
            # If mouse is away, set topmost (bring to front)
            self.root.attributes("-topmost", not mouse_in_proximity)

    def _update_score_decreasing_topmost(self):
        """Update window topmost state based on score decreasing.

        This only applies when always_on_top_while_score_decreasing is enabled.
        This takes priority over other topmost settings.

        Returns:
            bool: True if this behavior took control of topmost, False otherwise
        """
        # Only apply if the feature is enabled
        if not self.config.get_always_on_top_while_score_decreasing():
            return False  # Feature not enabled, no priority taken

        # Check if score is currently decreasing
        is_decreasing = self.score_tracker.is_score_decreasing()

        if is_decreasing:
            # Score is decreasing: force topmost to True
            self.root.attributes("-topmost", True)
            return True  # Priority taken, topmost is now True
        else:
            # Score is not decreasing: restore configured topmost behavior
            # This ensures we don't leave the window stuck in a forced topmost state
            self._apply_always_on_top()
            return False  # No priority, let other behaviors take over

    def _on_ctrl_c(self, event):
        """Handle CTRL+C key press to copy previous window title to clipboard.

        This copies the previous window title (not the current one) because when the user
        presses CTRL+C, the focus is on this application, making it the active window.
        What we want is the window that was active before switching to this app.

        Args:
            event: tkinter event object
        """
        if self._previous_window_title:
            try:
                # Clear clipboard and set new content
                self.root.clipboard_clear()
                self.root.clipboard_append(self._previous_window_title)
                # Update() is needed to finalize the clipboard operation
                self.root.update()
            except Exception as e:
                # Silently ignore clipboard errors to not disrupt the main functionality
                print(f"Warning: Failed to copy to clipboard: {e}")


class MockScoreDisplayWithColorTracking(MockScoreDisplay):
    """Extended mock for testing score color changes."""

    def __init__(self, score_tracker, window_monitor, config):
        super().__init__(score_tracker, config)
        self.window_monitor = window_monitor
        self._previous_score = score_tracker.get_score()
        self.score_label = MagicMock()

    def update_display_color_logic(self, window_title):
        """Simulate the color update logic from update_display."""
        # Update score
        self.score_tracker.update(window_title)

        # Get current score
        current_score = self.score_tracker.get_score()

        # Update score color based on score change
        if current_score < self._previous_score:
            # Score decreased - use score_down_color
            score_color = self.config.get_score_down_color()
        else:
            # Score increased or stayed the same - use score_up_color
            score_color = self.config.get_score_up_color()

        self.score_label.config(fg=score_color)
        self._previous_score = current_score

        return score_color


class MockScoreDisplayWithTransparency(MockScoreDisplay):
    """Extended mock for testing window transparency updates."""

    def __init__(self, score_tracker, config, update_interval=1000):
        super().__init__(score_tracker, config)
        self.update_interval = update_interval
        self._current_transparency = config.get_default_transparency()
        self._fade_active = False
        # Set initial transparency on the mock root
        self.root.attributes("-alpha", self._current_transparency)

    def _update_window_transparency(self):
        """Update window transparency based on flow mode state."""
        default_transparency = self.config.get_default_transparency()

        if not self.config.get_fade_window_on_flow_mode_enabled():
            # Mode is disabled, ensure window is at default transparency
            if self._current_transparency != default_transparency:
                self._current_transparency = default_transparency
                self.root.attributes("-alpha", self._current_transparency)
            self._fade_active = False
            return

        # Check if we're in flow state and should start fading
        flow_duration = self.score_tracker.get_flow_state_duration()
        flow_delay = self.config.get_flow_mode_delay_seconds()

        if self.score_tracker.is_in_flow_state() and flow_duration >= flow_delay:
            # We should be fading
            if not self._fade_active:
                # Just started fading
                self._fade_active = True

            # Calculate fade amount per update (update_interval is in ms, fade rate is per second)
            fade_per_update = (
                self.config.get_flow_mode_fade_rate_percent_per_second() / 100.0 * (self.update_interval / 1000.0)
            )

            # Apply fade (decrease transparency)
            new_transparency = max(0.0, self._current_transparency - fade_per_update)

            if new_transparency != self._current_transparency:
                self._current_transparency = new_transparency
                self.root.attributes("-alpha", self._current_transparency)
        else:
            # Not in flow state or haven't reached delay yet, reset transparency to default
            if self._current_transparency != default_transparency or self._fade_active:
                self._current_transparency = default_transparency
                self.root.attributes("-alpha", self._current_transparency)
                self._fade_active = False


class MockScoreDisplayWithStatusLabel(MockScoreDisplay):
    """Extended mock for testing status label updates."""

    def __init__(self, score_tracker, window_monitor, config):
        super().__init__(score_tracker, config)
        self.window_monitor = window_monitor
        self._previous_score = score_tracker.get_score()
        self.score_label = MagicMock()
        self.status_label = MagicMock()
        self._current_transparency = 1.0
        self._fade_active = False
        self.update_interval = 1000

    def update_display_status_logic(self, window_title):
        """Simulate the status label update logic from update_display."""
        # Update score
        score_changed, matched_pattern = self.score_tracker.update(window_title)

        # Update status label using the extracted function with elapsed seconds
        elapsed_seconds = self.score_tracker.get_current_window_elapsed_seconds()
        flow_mode_seconds = self.score_tracker.get_flow_mode_elapsed_seconds()
        status_text = get_status_text(
            matched_pattern, window_title, self.score_tracker.default_score, elapsed_seconds, flow_mode_seconds
        )
        self.status_label.config(text=status_text)
