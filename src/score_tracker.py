#!/usr/bin/env python3
"""Score tracking module for cat-window-watcher."""

from datetime import datetime

try:
    from .flow_state_manager import FlowStateManager
    from .score_calculator import ScoreCalculator
except ImportError:
    from flow_state_manager import FlowStateManager
    from score_calculator import ScoreCalculator


class ScoreTracker:
    """Track score based on window title matches."""

    def __init__(
        self,
        window_patterns,
        default_score=-1,
        apply_default_score_mode=True,
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
        reset_score_every_30_minutes=False,
        self_window_score=0,
        self_window_title="",
    ):
        """Initialize score tracker.

        Args:
            window_patterns: List of pattern dictionaries with regex, score, and description
            default_score: Score to apply when no pattern matches (default: -1)
            apply_default_score_mode: Whether to apply default score when no pattern matches (default: True)
            mild_penalty_mode: Whether to apply mild penalty during specified hours (default: False)
            mild_penalty_start_hour: Start hour for mild penalty mode (default: 22)
            mild_penalty_end_hour: End hour for mild penalty mode (default: 23)
            reset_score_every_30_minutes: Whether to reset score every 30 minutes (default: False)
            self_window_score: Score to apply when app's own window is active (default: 0)
            self_window_title: Title of app's own window (default: "")
        """
        # Initialize calculator and flow state manager
        self.calculator = ScoreCalculator(
            window_patterns,
            default_score,
            apply_default_score_mode,
            mild_penalty_mode,
            mild_penalty_start_hour,
            mild_penalty_end_hour,
            self_window_score,
            self_window_title,
        )
        self.flow_manager = FlowStateManager()

        # Store settings for getter methods
        self.default_score = default_score
        self.reset_score_every_30_minutes = reset_score_every_30_minutes

        # Score tracking state
        self.score = 0
        self.last_window_title = ""
        self.current_match = None
        self._last_reset_time_slot = self._get_current_time_slot() if reset_score_every_30_minutes else None
        self._current_window_start_time = datetime.now()  # Track when current window became active

    def update_config(
        self,
        window_patterns,
        default_score,
        apply_default_score_mode=True,
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
        reset_score_every_30_minutes=False,
        self_window_score=0,
        self_window_title="",
    ):
        """Update configuration patterns and settings.

        Args:
            window_patterns: List of pattern dictionaries with regex, score, and description
            default_score: Score to apply when no pattern matches
            apply_default_score_mode: Whether to apply default score when no pattern matches
            mild_penalty_mode: Whether to apply mild penalty during specified hours
            mild_penalty_start_hour: Start hour for mild penalty mode
            mild_penalty_end_hour: End hour for mild penalty mode
            reset_score_every_30_minutes: Whether to reset score every 30 minutes
            self_window_score: Score to apply when app's own window is active
            self_window_title: Title of app's own window
        """
        # Update calculator configuration
        self.calculator.update_config(
            window_patterns,
            default_score,
            apply_default_score_mode,
            mild_penalty_mode,
            mild_penalty_start_hour,
            mild_penalty_end_hour,
            self_window_score,
            self_window_title,
        )

        # Update local settings
        self.default_score = default_score
        self.reset_score_every_30_minutes = reset_score_every_30_minutes

        # Initialize last reset time slot if the feature is newly enabled
        if reset_score_every_30_minutes and self._last_reset_time_slot is None:
            self._last_reset_time_slot = self._get_current_time_slot()

    def _get_current_time_slot(self):
        """Get the current 30-minute time slot as a tuple (hour, half).

        Returns:
            tuple: (hour, half) where hour is 0-23 and half is 0 (for :00-:29) or 1 (for :30-:59)
        """
        now = datetime.now()
        hour = now.hour
        half = 0 if now.minute < 30 else 1
        return (hour, half)

    def _check_and_reset_if_needed(self):
        """Check if we've entered a new 30-minute time slot and reset score if needed."""
        if not self.reset_score_every_30_minutes:
            return

        current_time_slot = self._get_current_time_slot()

        # If time slot has changed, reset the score
        if self._last_reset_time_slot != current_time_slot:
            self.score = 0
            self._last_reset_time_slot = current_time_slot

    def update(self, window_title, is_screensaver=False):
        """Update score based on current window title.

        Args:
            window_title: Current active window title
            is_screensaver: Whether screensaver is currently active (default: False)

        Returns:
            tuple: (score_changed, current_match) where score_changed is bool
                   and current_match is the matched pattern dict or None
        """
        # Check if we need to reset score due to 30-minute time slot change
        self._check_and_reset_if_needed()

        score_changed = False
        previous_score = self.score

        # Track window change - reset start time when window title changes
        if self.last_window_title != window_title:
            self._current_window_start_time = datetime.now()

        # Update last window title
        self.last_window_title = window_title

        # Calculate score delta and get matched pattern
        score_delta, self.current_match = self.calculator.calculate_score_delta(
            window_title, is_screensaver, datetime.now()
        )

        # Apply score change
        if score_delta != 0:
            self.score += score_delta
            score_changed = True

        # Update flow state tracking
        self.flow_manager.update_flow_state(self.score, previous_score, datetime.now())

        return score_changed, self.current_match

    def get_flow_state_duration(self):
        """Get duration in seconds that we've been in score-up state.

        Returns:
            float: Duration in seconds, or 0 if not in score-up state
        """
        return self.flow_manager.get_flow_state_duration(datetime.now())

    def is_in_flow_state(self):
        """Check if currently in score-up state.

        Returns:
            bool: True if in score-up state, False otherwise
        """
        return self.flow_manager.is_in_flow_state()

    def is_score_decreasing(self):
        """Check if score is currently decreasing.

        Returns:
            bool: True if score is decreasing, False otherwise
        """
        return self.flow_manager.is_score_decreasing()

    def get_score(self):
        """Get current score.

        Returns:
            int: Current score
        """
        return self.score

    def reset_score(self):
        """Reset score to zero."""
        self.score = 0

    def get_current_match(self):
        """Get current matched pattern.

        Returns:
            dict: Current matched pattern or None
        """
        return self.current_match

    def get_current_window_elapsed_seconds(self):
        """Get elapsed seconds since current window became active.

        Returns:
            int: Elapsed seconds since current window became active
        """
        if self._current_window_start_time is None:
            return 0
        elapsed = (datetime.now() - self._current_window_start_time).total_seconds()
        return int(elapsed)

    def get_flow_mode_elapsed_seconds(self):
        """Get elapsed seconds since flow mode started if in flow state, otherwise 0.

        Returns:
            int: Elapsed seconds since flow mode started, or 0 if not in flow state
        """
        return self.flow_manager.get_flow_mode_elapsed_seconds(datetime.now())
