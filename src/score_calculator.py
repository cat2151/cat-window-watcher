#!/usr/bin/env python3
"""Score calculation module for cat-window-watcher."""

import re


class ScoreCalculator:
    """Calculator for score changes based on window patterns and time-based rules."""

    def __init__(
        self,
        window_patterns,
        default_score=-1,
        apply_default_score_mode=True,
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
        self_window_score=0,
        self_window_title="",
    ):
        """Initialize score calculator.

        Args:
            window_patterns: List of pattern dictionaries with regex, score, and description
            default_score: Score to apply when no pattern matches (default: -1)
            apply_default_score_mode: Whether to apply default score when no pattern matches (default: True)
            mild_penalty_mode: Whether to apply mild penalty during specified hours (default: False)
            mild_penalty_start_hour: Start hour for mild penalty mode (default: 22)
            mild_penalty_end_hour: End hour for mild penalty mode (default: 23)
            self_window_score: Score to apply when app's own window is active (default: 0)
            self_window_title: Title of app's own window (default: "")
        """
        self.window_patterns = window_patterns
        self.default_score = default_score
        self.apply_default_score_mode = apply_default_score_mode
        self.mild_penalty_mode = mild_penalty_mode
        self.mild_penalty_start_hour = mild_penalty_start_hour
        self.mild_penalty_end_hour = mild_penalty_end_hour
        self.self_window_score = self_window_score
        self.self_window_title = self_window_title

    def update_config(
        self,
        window_patterns,
        default_score,
        apply_default_score_mode=True,
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
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
            self_window_score: Score to apply when app's own window is active
            self_window_title: Title of app's own window
        """
        self.window_patterns = window_patterns
        self.default_score = default_score
        self.apply_default_score_mode = apply_default_score_mode
        self.mild_penalty_mode = mild_penalty_mode
        self.mild_penalty_start_hour = mild_penalty_start_hour
        self.mild_penalty_end_hour = mild_penalty_end_hour
        self.self_window_score = self_window_score
        self.self_window_title = self_window_title

    def calculate_score_delta(self, window_title, is_screensaver=False, datetime_now=None):
        """Calculate score delta based on window title and current state.

        Args:
            window_title: Current active window title
            is_screensaver: Whether screensaver is currently active (default: False)
            datetime_now: Current datetime (for testing), or None to use real datetime

        Returns:
            tuple: (score_delta, matched_pattern) where score_delta is the score change
                   and matched_pattern is the matched pattern dict or None
        """
        # If screensaver is active, don't change score (score delta = 0)
        if is_screensaver:
            # Mark as matched with score 0 to prevent default_score from being applied
            matched_pattern = {
                "regex": "",
                "score": 0,
                "description": "スクリーンセーバー",
            }
            return 0, matched_pattern

        # Check if this is the app's own window
        if self.self_window_title and window_title == self.self_window_title:
            # Apply mild penalty to self window score if applicable
            adjusted_self_window_score = self._apply_mild_penalty(self.self_window_score, datetime_now)
            # Mark as matched (even if score is 0) to prevent default_score from being applied
            matched_pattern = {
                "regex": "",
                "score": self.self_window_score,
                "description": "Cat Window Watcher (self)",
            }
            return adjusted_self_window_score, matched_pattern

        # Check each pattern against window title
        for pattern in self.window_patterns:
            regex = pattern.get("regex", "")
            score_delta = pattern.get("score", 0)

            if regex and re.search(regex, window_title, re.IGNORECASE):
                # Apply mild penalty if applicable
                adjusted_score_delta = self._apply_mild_penalty(score_delta, datetime_now)
                return adjusted_score_delta, pattern

        # If no pattern matched, apply default score (if mode is enabled)
        if self.apply_default_score_mode and self.default_score != 0:
            # Apply mild penalty to default score if applicable
            adjusted_default_score = self._apply_mild_penalty(self.default_score, datetime_now)
            return adjusted_default_score, None

        # No match and default score mode disabled or default score is 0
        return 0, None

    def _is_in_mild_penalty_hours(self, datetime_now=None):
        """Check if current time is within mild penalty hours.

        Args:
            datetime_now: Current datetime (for testing), or None to use real datetime

        Returns:
            bool: True if current time is within mild penalty hours, False otherwise
        """
        if not self.mild_penalty_mode:
            return False

        # Import datetime here to support mocking
        if datetime_now is None:
            from datetime import datetime

            datetime_now = datetime.now()

        current_hour = datetime_now.hour

        # Handle time range that wraps around midnight
        if self.mild_penalty_start_hour <= self.mild_penalty_end_hour:
            # Normal range (e.g., 22:00-23:59)
            return self.mild_penalty_start_hour <= current_hour <= self.mild_penalty_end_hour
        else:
            # Wrapped range (e.g., 23:00-01:00)
            return current_hour >= self.mild_penalty_start_hour or current_hour <= self.mild_penalty_end_hour

    def _apply_mild_penalty(self, score_delta, datetime_now=None):
        """Apply mild penalty if conditions are met.

        Args:
            score_delta: Original score delta
            datetime_now: Current datetime (for testing), or None to use real datetime

        Returns:
            int: Modified score delta (-1 if negative during mild penalty hours, otherwise original)
        """
        if self._is_in_mild_penalty_hours(datetime_now) and score_delta < 0:
            return -1
        return score_delta
