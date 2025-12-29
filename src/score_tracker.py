#!/usr/bin/env python3
"""Score tracking module for cat-window-watcher."""

import re
from datetime import datetime


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
        """
        self.window_patterns = window_patterns
        self.default_score = default_score
        self.apply_default_score_mode = apply_default_score_mode
        self.mild_penalty_mode = mild_penalty_mode
        self.mild_penalty_start_hour = mild_penalty_start_hour
        self.mild_penalty_end_hour = mild_penalty_end_hour
        self.reset_score_every_30_minutes = reset_score_every_30_minutes
        self.score = 0
        self.last_window_title = ""
        self.current_match = None
        self._last_reset_time_slot = self._get_current_time_slot() if reset_score_every_30_minutes else None
        self._in_score_up_state = False
        self._score_up_state_start_time = None

    def update_config(
        self,
        window_patterns,
        default_score,
        apply_default_score_mode=True,
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
        reset_score_every_30_minutes=False,
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
        """
        self.window_patterns = window_patterns
        self.default_score = default_score
        self.apply_default_score_mode = apply_default_score_mode
        self.mild_penalty_mode = mild_penalty_mode
        self.mild_penalty_start_hour = mild_penalty_start_hour
        self.mild_penalty_end_hour = mild_penalty_end_hour
        self.reset_score_every_30_minutes = reset_score_every_30_minutes

        # Initialize last reset time slot if the feature is newly enabled
        if reset_score_every_30_minutes and self._last_reset_time_slot is None:
            self._last_reset_time_slot = self._get_current_time_slot()

    def _is_in_mild_penalty_hours(self):
        """Check if current time is within mild penalty hours.

        Returns:
            bool: True if current time is within mild penalty hours, False otherwise
        """
        if not self.mild_penalty_mode:
            return False

        current_hour = datetime.now().hour

        # Handle time range that wraps around midnight
        if self.mild_penalty_start_hour <= self.mild_penalty_end_hour:
            # Normal range (e.g., 22:00-23:59)
            return self.mild_penalty_start_hour <= current_hour <= self.mild_penalty_end_hour
        else:
            # Wrapped range (e.g., 23:00-01:00)
            return current_hour >= self.mild_penalty_start_hour or current_hour <= self.mild_penalty_end_hour

    def _apply_mild_penalty(self, score_delta):
        """Apply mild penalty if conditions are met.

        Args:
            score_delta: Original score delta

        Returns:
            int: Modified score delta (-1 if negative during mild penalty hours, otherwise original)
        """
        if self._is_in_mild_penalty_hours() and score_delta < 0:
            return -1
        return score_delta

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

    def update(self, window_title):
        """Update score based on current window title.

        Args:
            window_title: Current active window title

        Returns:
            tuple: (score_changed, current_match) where score_changed is bool
                   and current_match is the matched pattern dict or None
        """
        # Check if we need to reset score due to 30-minute time slot change
        self._check_and_reset_if_needed()

        score_changed = False
        self.current_match = None
        previous_score = self.score

        # Update last window title
        self.last_window_title = window_title

        # Check each pattern against window title
        for pattern in self.window_patterns:
            regex = pattern.get("regex", "")
            score_delta = pattern.get("score", 0)

            if regex and re.search(regex, window_title, re.IGNORECASE):
                # Apply mild penalty if applicable
                adjusted_score_delta = self._apply_mild_penalty(score_delta)
                self.score += adjusted_score_delta
                self.current_match = pattern
                score_changed = True
                break  # Only match first pattern

        # If no pattern matched, apply default score (if mode is enabled)
        if not self.current_match and self.apply_default_score_mode and self.default_score != 0:
            # Apply mild penalty to default score if applicable
            adjusted_default_score = self._apply_mild_penalty(self.default_score)
            self.score += adjusted_default_score
            score_changed = True

        # Update flow state tracking
        self._update_flow_state(previous_score)

        return score_changed, self.current_match

    def _update_flow_state(self, previous_score):
        """Update flow state based on score changes.

        Args:
            previous_score: Score before the current update
        """
        current_score = self.score
        was_in_score_up = self._in_score_up_state

        # Enter flow (score-up) state only when score actually increases.
        # Maintain flow state when score does not decrease and we are already in flow.
        if current_score > previous_score:
            # Score increased: transition from non-score-up to score-up if needed
            if not was_in_score_up:
                self._in_score_up_state = True
                self._score_up_state_start_time = datetime.now()
        elif current_score < previous_score:
            # Score decreased: leave flow state
            self._in_score_up_state = False
            self._score_up_state_start_time = None
        # If current_score == previous_score, we intentionally keep the existing
        # flow state as-is: maintain if already in flow, remain out otherwise.

    def get_flow_state_duration(self):
        """Get duration in seconds that we've been in score-up state.

        Returns:
            float: Duration in seconds, or 0 if not in score-up state
        """
        if not self._in_score_up_state or self._score_up_state_start_time is None:
            return 0.0

        duration = (datetime.now() - self._score_up_state_start_time).total_seconds()
        return duration

    def is_in_flow_state(self):
        """Check if currently in score-up state.

        Returns:
            bool: True if in score-up state, False otherwise
        """
        return self._in_score_up_state

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
