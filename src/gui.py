#!/usr/bin/env python3
"""GUI module for cat-window-watcher using tkinter."""

import tkinter as tk

try:
    from .constants import APP_WINDOW_TITLE
    from .status_formatter import StatusFormatter
    from .window_behavior import WindowBehaviorManager
except ImportError:
    from constants import APP_WINDOW_TITLE
    from status_formatter import StatusFormatter
    from window_behavior import WindowBehaviorManager


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
        self.default_update_interval = update_interval  # Store original interval
        self.is_game_playing = False  # Track game playing state

        # Track previous score for color changes
        self._previous_score = score_tracker.get_score()

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

        # Initialize window behavior manager
        self.behavior_manager = WindowBehaviorManager(self.root, config, score_tracker)

        # Set initial transparency
        self.root.attributes("-alpha", self.behavior_manager.get_current_transparency())

        # Apply initial always_on_top setting
        self.behavior_manager.apply_always_on_top()

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
            self.behavior_manager.apply_always_on_top()

        # Check for game playing detection
        game_detection = self.config.get_game_playing_detection()

        if game_detection["enabled"]:
            # Get active process name
            process_name = self.window_monitor.get_active_window_process_name()

            # Check if the current process matches any configured game process
            is_game_playing_now = process_name in game_detection["process_names"]

            # Handle transition into game playing mode
            if is_game_playing_now and not self.is_game_playing:
                # Entering game playing mode - switch to longer interval
                self.is_game_playing = True
                self.update_interval = game_detection["check_interval_seconds"] * 1000  # Convert to milliseconds
                print(
                    f"Game detected ({process_name}), switching to {game_detection['check_interval_seconds']} second check interval"
                )
            # Handle transition out of game playing mode
            elif not is_game_playing_now and self.is_game_playing:
                # Exiting game playing mode - switch back to normal interval
                self.is_game_playing = False
                self.update_interval = self.default_update_interval
                print(f"Game ended, switching back to {self.default_update_interval // 1000} second check interval")

        # Get current window title
        window_title = self.window_monitor.get_active_window_title()

        # Check if screensaver is active
        debug_screensaver = self.config.get_debug_screensaver_detection()
        if debug_screensaver:
            print("=" * 60)
            print("[DEBUG] Screensaver detection check:")
            print(f"[DEBUG]   - Current window title: '{window_title}'")

        is_screensaver = self.window_monitor.is_screensaver_active(debug=debug_screensaver)

        if debug_screensaver:
            print("=" * 60)

        # Store previous window title before updating to current
        # This is used for clipboard operations (CTRL+C)
        # Only update previous title if current title is non-empty to avoid
        # losing the last valid title when window monitoring temporarily fails
        if self._current_window_title:
            self._previous_window_title = self._current_window_title

        # Store current window title
        self._current_window_title = window_title

        # Update score
        score_changed, matched_pattern = self.score_tracker.update(window_title, is_screensaver=is_screensaver)

        # Update score-decreasing-based topmost behavior (after score update)
        # This has highest priority - if it takes control, skip other topmost updates
        if not self.behavior_manager.update_score_decreasing_topmost():
            # Score decreasing didn't take priority, apply other topmost behaviors
            # Update proximity-based topmost behavior
            self.behavior_manager.update_proximity_based_topmost()

        # Update window transparency based on flow mode
        self.behavior_manager.update_window_transparency(self.update_interval)

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
        flow_mode_seconds = self.score_tracker.get_flow_mode_elapsed_seconds()
        status_text = StatusFormatter.format_status_text(
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
