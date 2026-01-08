#!/usr/bin/env python3
"""Window behavior management module for cat-window-watcher GUI."""


class WindowBehaviorManager:
    """Manager for window behavior including transparency, topmost, and mouse proximity."""

    def __init__(self, root, config, score_tracker):
        """Initialize window behavior manager.

        Args:
            root: tkinter root window
            config: Config instance
            score_tracker: ScoreTracker instance
        """
        self.root = root
        self.config = config
        self.score_tracker = score_tracker

        # Track previous always_on_top state for dynamic updates
        self._previous_always_on_top = None

        # Track mouse proximity state
        self._mouse_in_proximity = False

        # Track fade state for flow mode
        self._current_transparency = config.get_default_transparency()
        self._fade_active = False

    def apply_always_on_top(self):
        """Apply always_on_top setting to the window."""
        current_always_on_top = self.config.get_always_on_top()

        # Only update if the setting has changed
        if current_always_on_top != self._previous_always_on_top:
            self.root.attributes("-topmost", current_always_on_top)
            self._previous_always_on_top = current_always_on_top

    def is_mouse_in_proximity(self):
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

    def update_proximity_based_topmost(self):
        """Update window topmost state based on mouse proximity.

        This only applies when both always_on_top and hide_on_mouse_proximity are enabled.
        """
        # Only apply proximity-based behavior if both settings are enabled
        if not self.config.get_always_on_top() or not self.config.get_hide_on_mouse_proximity():
            return

        # Check if mouse is in proximity
        mouse_in_proximity = self.is_mouse_in_proximity()

        # Update topmost state if proximity state changed
        if mouse_in_proximity != self._mouse_in_proximity:
            self._mouse_in_proximity = mouse_in_proximity

            # If mouse is in proximity, remove topmost (send to back)
            # If mouse is away, set topmost (bring to front)
            self.root.attributes("-topmost", not mouse_in_proximity)

    def update_score_decreasing_topmost(self):
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
            self.apply_always_on_top()
            return False  # No priority, let other behaviors take over

    def update_window_transparency(self, update_interval):
        """Update window transparency based on flow mode state.

        Args:
            update_interval: Update interval in milliseconds
        """
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
                self.config.get_flow_mode_fade_rate_percent_per_second() / 100.0 * (update_interval / 1000.0)
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

    def get_current_transparency(self):
        """Get current window transparency.

        Returns:
            float: Current transparency value (0.0-1.0)
        """
        return self._current_transparency

    def reset_transparency(self):
        """Reset window transparency to default value."""
        default_transparency = self.config.get_default_transparency()
        self._current_transparency = default_transparency
        self.root.attributes("-alpha", self._current_transparency)
        self._fade_active = False
