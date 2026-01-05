#!/usr/bin/env python3
"""GUI module for cat-window-watcher using tkinter."""

import tkinter as tk

try:
    from .constants import APP_WINDOW_TITLE
except ImportError:
    from constants import APP_WINDOW_TITLE

# Maximum window title length before truncation
MAX_WINDOW_TITLE_LENGTH = 40


def get_status_text(matched_pattern, window_title, default_score, elapsed_seconds=0, flow_mode_seconds=0):
    """Generate status text based on pattern match and window title.

    Args:
        matched_pattern: Matched pattern dict with 'description' and 'score', or None
        window_title: Current window title string
        default_score: Default score value when no pattern matches
        elapsed_seconds: Elapsed seconds since current window became active (default: 0)
        flow_mode_seconds: Elapsed seconds since flow mode started (default: 0)

    Returns:
        str: Status text to display
    """
    # Format elapsed time - prioritize flow mode time if active
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
        # No match - always show window title to help users configure patterns
        # Show truncated window title
        display_title = (
            window_title[:MAX_WINDOW_TITLE_LENGTH] + "..."
            if len(window_title) > MAX_WINDOW_TITLE_LENGTH
            else window_title
        )

        # Check if default score was applied
        if default_score != 0:
            score_sign = "+" if default_score >= 0 else ""
            score_text = f"({score_sign}{default_score})"
            # Combine window title with default score information
            return (
                f"No match: {display_title} {score_text}{elapsed_text}"
                if display_title
                else f"No match {score_text}{elapsed_text}"
            )
        else:
            return f"{display_title}{elapsed_text}" if display_title else f"Watching...{elapsed_text}"


class ScoreDisplay:
    """Tkinter GUI for displaying score."""

    def __init__(self, score_tracker, window_monitor, config, update_interval=1000):
        """Initialize score display.

        Args:
            score_tracker: ScoreTracker instance
            window_monitor: WindowMonitor instance
            config: Config instance
            update_interval: Update interval in milliseconds (default: 1000ms = 1 second)
        """
        self.score_tracker = score_tracker
        self.window_monitor = window_monitor
        self.config = config
        self.update_interval = update_interval

        # Track previous always_on_top state for dynamic updates
        self._previous_always_on_top = None

        # Track mouse proximity state
        self._mouse_in_proximity = False

        # Track previous score for color changes
        self._previous_score = score_tracker.get_score()

        # Track fade state for flow mode
        # Initialize transparency from config
        self._current_transparency = config.get_default_transparency()
        self._fade_active = False

        # Track current and previous window title for clipboard operations
        self._current_window_title = ""
        self._previous_window_title = ""

        # Create main window
        self.root = tk.Tk()
        self.root.title(APP_WINDOW_TITLE)

        # Set window geometry (size and optionally position)
        window_x = config.get_window_x()
        window_y = config.get_window_y()
        if window_x is not None and window_y is not None:
            self.root.geometry(f"400x200+{window_x}+{window_y}")
        else:
            self.root.geometry("400x200")

        self.root.configure(bg="#2b2b2b")

        # Set initial transparency
        self.root.attributes("-alpha", self._current_transparency)

        # Apply initial always_on_top setting
        self._apply_always_on_top()

        # Bind clipboard copy shortcuts (Ctrl+C on Windows/Linux, Command+C on macOS)
        self.root.bind("<Control-c>", self._on_ctrl_c)
        self.root.bind("<Command-c>", self._on_ctrl_c)

        # Create score label with initial color
        initial_color = config.get_score_up_color()
        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 48, "bold"),
            fg=initial_color,
            bg="#2b2b2b",
        )
        self.score_label.pack(expand=True)

        # Create status label
        self.status_label = tk.Label(
            self.root,
            text="Watching...",
            font=("Arial", 12),
            fg="#888888",
            bg="#2b2b2b",
        )
        self.status_label.pack(pady=10)

    def _apply_always_on_top(self):
        """Apply always_on_top setting to the window."""
        current_always_on_top = self.config.get_always_on_top()

        # Only update if the setting has changed
        if current_always_on_top != self._previous_always_on_top:
            self.root.attributes("-topmost", current_always_on_top)
            self._previous_always_on_top = current_always_on_top

    def _is_mouse_in_proximity(self):
        """Check if mouse is within proximity distance of the window.

        Returns:
            bool: True if mouse is within proximity distance, False otherwise
        """
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
        """Update window topmost state based on mouse proximity.

        This only applies when both always_on_top and hide_on_mouse_proximity are enabled.
        """
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

    def update_display(self):
        """Update the display with current score and window info."""
        # Check if config file has been modified and reload if necessary
        if self.config.reload_if_modified():
            # Update score tracker with new configuration
            self.score_tracker.update_config(
                self.config.get_window_patterns(),
                self.config.get_default_score(),
                self.config.get_apply_default_score_mode(),
                self.config.get_mild_penalty_mode(),
                self.config.get_mild_penalty_start_hour(),
                self.config.get_mild_penalty_end_hour(),
                self.config.get_reset_score_every_30_minutes(),
                self.config.get_self_window_score(),
                APP_WINDOW_TITLE,
            )

            # Update always_on_top setting if it changed
            self._apply_always_on_top()

        # Get current window title
        window_title = self.window_monitor.get_active_window_title()

        # Store previous window title before updating to current
        # This is used for clipboard operations (CTRL+C)
        # Only update previous title if current title is non-empty to avoid
        # losing the last valid title when window monitoring temporarily fails
        if self._current_window_title:
            self._previous_window_title = self._current_window_title

        # Store current window title
        self._current_window_title = window_title

        # Update score
        score_changed, matched_pattern = self.score_tracker.update(window_title)

        # Update score-decreasing-based topmost behavior (after score update)
        # This has highest priority - if it takes control, skip other topmost updates
        if not self._update_score_decreasing_topmost():
            # Score decreasing didn't take priority, apply other topmost behaviors
            # Update proximity-based topmost behavior
            self._update_proximity_based_topmost()

        # Update window transparency based on flow mode
        self._update_window_transparency()

        # Update score label
        current_score = self.score_tracker.get_score()
        self.score_label.config(text=f"Score: {current_score}")

        # Update score color based on score change
        if current_score < self._previous_score:
            # Score decreased - use score_down_color
            score_color = self.config.get_score_down_color()
        else:
            # Score increased or stayed the same - use score_up_color
            score_color = self.config.get_score_up_color()

        self.score_label.config(fg=score_color)
        self._previous_score = current_score

        # Update status label with elapsed seconds
        elapsed_seconds = self.score_tracker.get_current_window_elapsed_seconds()
        flow_mode_seconds = (
            int(self.score_tracker.get_flow_state_duration()) if self.score_tracker.is_in_flow_state() else 0
        )
        status_text = get_status_text(
            matched_pattern, window_title, self.score_tracker.default_score, elapsed_seconds, flow_mode_seconds
        )
        self.status_label.config(text=status_text)

        # Schedule next update
        self.root.after(self.update_interval, self.update_display)

    def run(self):
        """Run the GUI main loop."""
        # Start the update cycle
        self.update_display()

        # Start tkinter main loop
        self.root.mainloop()
