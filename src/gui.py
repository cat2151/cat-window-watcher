#!/usr/bin/env python3
"""GUI module for cat-window-watcher using tkinter."""

import tkinter as tk


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

        # Create main window
        self.root = tk.Tk()
        self.root.title("Cat Window Watcher - Cat is watching you -")
        self.root.geometry("400x200")
        self.root.configure(bg="#2b2b2b")

        # Apply always_on_top setting if configured
        if self.config.get_always_on_top():
            self.root.attributes("-topmost", True)

        # Create score label
        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 48, "bold"),
            fg="#ffffff",
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

    def update_display(self):
        """Update the display with current score and window info."""
        # Check if config file has been modified and reload if necessary
        if self.config.reload_if_modified():
            # Update score tracker with new configuration
            self.score_tracker.update_config(self.config.get_window_patterns(), self.config.get_default_score())

        # Get current window title
        window_title = self.window_monitor.get_active_window_title()

        # Update score
        score_changed, matched_pattern = self.score_tracker.update(window_title)

        # Update score label
        current_score = self.score_tracker.get_score()
        self.score_label.config(text=f"Score: {current_score}")

        # Update status label
        if matched_pattern:
            description = matched_pattern.get("description", "")
            score_delta = matched_pattern.get("score", 0)
            score_sign = "+" if score_delta >= 0 else ""
            self.status_label.config(text=f"{description} ({score_sign}{score_delta})")
        else:
            # Check if default score was applied
            default_score = self.score_tracker.default_score
            if default_score != 0:
                score_sign = "+" if default_score >= 0 else ""
                self.status_label.config(text=f"No match ({score_sign}{default_score})")
            else:
                # Show truncated window title
                display_title = window_title[:40] + "..." if len(window_title) > 40 else window_title
                self.status_label.config(text=display_title if display_title else "Watching...")

        # Schedule next update
        self.root.after(self.update_interval, self.update_display)

    def run(self):
        """Run the GUI main loop."""
        # Start the update cycle
        self.update_display()

        # Start tkinter main loop
        self.root.mainloop()
