#!/usr/bin/env python3
"""Flow state management module for cat-window-watcher."""


class FlowStateManager:
    """Manager for flow state tracking and score decrease detection."""

    def __init__(self):
        """Initialize flow state manager."""
        self._in_score_up_state = False
        self._score_up_state_start_time = None
        self._in_score_decreasing_state = False

    def update_flow_state(self, current_score, previous_score, datetime_now=None):
        """Update flow state based on score changes.

        Args:
            current_score: Current score value
            previous_score: Score value before the current update
            datetime_now: Current datetime (for testing), or None to use real datetime
        """
        # Import datetime here to support mocking
        if datetime_now is None:
            from datetime import datetime

            datetime_now = datetime.now()

        was_in_score_up = self._in_score_up_state

        # Enter flow (score-up) state only when score actually increases.
        # Once in flow, maintain it when score stays equal (but not on initial equal scores).
        if current_score > previous_score:
            # Score increased: transition from non-score-up to score-up if needed
            if not was_in_score_up:
                self._in_score_up_state = True
                self._score_up_state_start_time = datetime_now
            # Score increased: leave score-decreasing state
            self._in_score_decreasing_state = False
        elif current_score < previous_score:
            # Score decreased: leave flow state
            self._in_score_up_state = False
            self._score_up_state_start_time = None
            # Score decreased: enter score-decreasing state
            self._in_score_decreasing_state = True
        else:
            # Score stayed the same: leave score-decreasing state
            self._in_score_decreasing_state = False
        # If current_score == previous_score, we intentionally keep the existing
        # flow state as-is (maintain if already in flow, remain out otherwise),
        # while also clearing any active score-decreasing state.

    def get_flow_state_duration(self, datetime_now=None):
        """Get duration in seconds that we've been in score-up state.

        Args:
            datetime_now: Current datetime (for testing), or None to use real datetime

        Returns:
            float: Duration in seconds, or 0 if not in score-up state
        """
        if not self._in_score_up_state or self._score_up_state_start_time is None:
            return 0.0

        # Import datetime here to support mocking
        if datetime_now is None:
            from datetime import datetime

            datetime_now = datetime.now()

        duration = (datetime_now - self._score_up_state_start_time).total_seconds()
        return duration

    def is_in_flow_state(self):
        """Check if currently in score-up state.

        Returns:
            bool: True if in score-up state, False otherwise
        """
        return self._in_score_up_state

    def is_score_decreasing(self):
        """Check if score is currently decreasing.

        Returns:
            bool: True if score is decreasing, False otherwise
        """
        return self._in_score_decreasing_state

    def get_flow_mode_elapsed_seconds(self, datetime_now=None):
        """Get elapsed seconds since flow mode started if in flow state, otherwise 0.

        Args:
            datetime_now: Current datetime (for testing), or None to use real datetime

        Returns:
            int: Elapsed seconds since flow mode started, or 0 if not in flow state
        """
        if self.is_in_flow_state():
            return int(self.get_flow_state_duration(datetime_now))
        return 0
