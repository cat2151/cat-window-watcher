#!/usr/bin/env python3
"""Score tracking module for cat-window-watcher."""

import re


class ScoreTracker:
    """Track score based on window title matches."""

    def __init__(self, window_patterns):
        """Initialize score tracker.

        Args:
            window_patterns: List of pattern dictionaries with regex, score, and description
        """
        self.window_patterns = window_patterns
        self.score = 0
        self.last_window_title = ""
        self.current_match = None

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

        # Only update if window title changed
        if window_title != self.last_window_title:
            self.last_window_title = window_title

            # Check each pattern against window title
            for pattern in self.window_patterns:
                regex = pattern.get("regex", "")
                score_delta = pattern.get("score", 0)

                if regex and re.search(regex, window_title, re.IGNORECASE):
                    self.score += score_delta
                    self.current_match = pattern
                    score_changed = True
                    break  # Only match first pattern

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
