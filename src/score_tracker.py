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
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
    ):
        """Initialize score tracker.

        Args:
            window_patterns: List of pattern dictionaries with regex, score, and description
            default_score: Score to apply when no pattern matches (default: -1)
            mild_penalty_mode: Whether to apply mild penalty during specified hours (default: False)
            mild_penalty_start_hour: Start hour for mild penalty mode (default: 22)
            mild_penalty_end_hour: End hour for mild penalty mode (default: 23)
        """
        self.window_patterns = window_patterns
        self.default_score = default_score
        self.mild_penalty_mode = mild_penalty_mode
        self.mild_penalty_start_hour = mild_penalty_start_hour
        self.mild_penalty_end_hour = mild_penalty_end_hour
        self.score = 0
        self.last_window_title = ""
        self.current_match = None

    def update_config(
        self,
        window_patterns,
        default_score,
        mild_penalty_mode=False,
        mild_penalty_start_hour=22,
        mild_penalty_end_hour=23,
    ):
        """Update configuration patterns and settings.

        Args:
            window_patterns: List of pattern dictionaries with regex, score, and description
            default_score: Score to apply when no pattern matches
            mild_penalty_mode: Whether to apply mild penalty during specified hours
            mild_penalty_start_hour: Start hour for mild penalty mode
            mild_penalty_end_hour: End hour for mild penalty mode
        """
        self.window_patterns = window_patterns
        self.default_score = default_score
        self.mild_penalty_mode = mild_penalty_mode
        self.mild_penalty_start_hour = mild_penalty_start_hour
        self.mild_penalty_end_hour = mild_penalty_end_hour

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

    def update(self, window_title):
        """Update score based on current window title.

        Args:
            window_title: Current active window title

        Returns:
            tuple: (score_changed, current_match) where score_changed is bool
                   and current_match is the matched pattern dict or None
        """
        score_changed = False
        self.current_match = None

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

        # If no pattern matched, apply default score
        if not self.current_match and self.default_score != 0:
            # Apply mild penalty to default score if applicable
            adjusted_default_score = self._apply_mild_penalty(self.default_score)
            self.score += adjusted_default_score
            score_changed = True

        return score_changed, self.current_match

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
