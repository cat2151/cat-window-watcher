#!/usr/bin/env python3
"""Tests for score tracker module - score reset and score decreasing state."""

import unittest
from pathlib import Path

try:
    from src.score_tracker import ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from score_tracker import ScoreTracker

# Use module path derived from the actual import so patch() works in all environments.
_SCORE_TRACKER_DATETIME_PATH = f"{ScoreTracker.__module__}.datetime"


class TestResetScoreEvery30Minutes(unittest.TestCase):
    """Test cases for reset score every 30 minutes functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
        ]

    def test_reset_mode_disabled(self):
        """Test that score does not reset when mode is disabled."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=False,
        )

        # Mock datetime to return 10:29
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 29)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Move to 10:30 (new time slot) - score should NOT reset
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 30)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 20)

    def test_reset_at_30_minute_boundary(self):
        """Test that score resets at :30 boundary when mode is enabled."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Mock datetime to return 10:29
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 29)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Move to 10:30 (new time slot) - score should reset to 0, then add 10
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 30)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

    def test_reset_at_00_minute_boundary(self):
        """Test that score resets at :00 boundary when mode is enabled."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Mock datetime to return 10:59
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 59)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Move to 11:00 (new time slot) - score should reset to 0, then add 10
            mock_datetime.now.return_value = datetime(2024, 1, 1, 11, 0)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

    def test_no_reset_within_same_time_slot(self):
        """Test that score accumulates normally within the same 30-minute time slot."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Mock datetime to return 10:15
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 15)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Move to 10:20 (same time slot) - score should accumulate
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 20)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 20)

            # Move to 10:29 (still same time slot) - score should accumulate
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 29)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 30)

    def test_reset_across_hour_boundary(self):
        """Test that score resets correctly when crossing from one hour to the next."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Start at 9:45 (second half of hour 9)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 9, 45)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Move to 10:00 (first half of hour 10) - different time slot
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)  # Reset happened

    def test_reset_with_negative_scores(self):
        """Test that reset works correctly with negative scores."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Accumulate negative score
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 15)
            tracker.update("Twitter Feed")
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -10)

            # Move to next time slot - score should reset to 0
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 30)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

    def test_reset_at_midnight(self):
        """Test that reset works correctly at midnight (hour 0)."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Start at 23:50 (second half of hour 23)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 23, 50)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Move to 00:00 (first half of hour 0, next day) - different time slot
            mock_datetime.now.return_value = datetime(2024, 1, 2, 0, 0)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)  # Reset happened

    def test_update_config_enables_reset(self):
        """Test that update_config can enable reset mode."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=False,
        )

        # Build up score without reset
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 29)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Enable reset mode
            tracker.update_config(
                self.patterns,
                default_score=0,
                reset_score_every_30_minutes=True,
            )

            # Move to next time slot - score should reset
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 30)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)  # Reset happened

    def test_update_config_disables_reset(self):
        """Test that update_config can disable reset mode."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        # Build up score
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 29)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Disable reset mode
            tracker.update_config(
                self.patterns,
                default_score=0,
                reset_score_every_30_minutes=False,
            )

            # Move to next time slot - score should NOT reset
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 30)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 20)  # No reset

    def test_multiple_resets_across_several_time_slots(self):
        """Test that score resets correctly across multiple time slots."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            # Time slot 1: 10:00-10:29
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 15)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Time slot 2: 10:30-10:59 - reset should occur
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 45)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Time slot 3: 11:00-11:29 - reset should occur again
            mock_datetime.now.return_value = datetime(2024, 1, 1, 11, 15)
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

    def test_reset_with_mixed_positive_and_negative_scores(self):
        """Test reset with a mix of positive and negative scores."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=0,
            reset_score_every_30_minutes=True,
        )

        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            # Build up mixed score
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 15)
            tracker.update("GitHub")  # +10
            tracker.update("Twitter Feed")  # -5
            tracker.update("GitHub")  # +10
            self.assertEqual(tracker.get_score(), 15)

            # Move to next time slot - score should reset
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 30)
            tracker.update("Twitter Feed")  # -5 (after reset)
            self.assertEqual(tracker.get_score(), -5)


class TestScoreDecreasingState(unittest.TestCase):
    """Test cases for score decreasing state tracking."""

    def test_initial_score_decreasing_state(self):
        """Test score decreasing state is initially False."""
        tracker = ScoreTracker([{"regex": "github", "score": 10, "description": "GitHub"}])
        self.assertFalse(tracker.is_score_decreasing())


class TestScoreDecreasingStateContinued(unittest.TestCase):
    """Additional test cases for score decreasing state tracking."""

    def test_score_decreasing_state_on_score_decrease(self):
        """Test score decreasing state is True when score decreases."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        tracker = ScoreTracker(patterns, default_score=0)

        # Increase score first
        tracker.update("GitHub")
        self.assertEqual(tracker.get_score(), 10)
        self.assertFalse(tracker.is_score_decreasing())

        # Decrease score
        tracker.update("Twitter")
        self.assertEqual(tracker.get_score(), 5)
        self.assertTrue(tracker.is_score_decreasing())

    def test_score_decreasing_state_on_score_increase(self):
        """Test score decreasing state is False when score increases."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        tracker = ScoreTracker(patterns, default_score=0)

        # Decrease score first
        tracker.update("Twitter")
        self.assertEqual(tracker.get_score(), -5)
        self.assertTrue(tracker.is_score_decreasing())

        # Increase score
        tracker.update("GitHub")
        self.assertEqual(tracker.get_score(), 5)
        self.assertFalse(tracker.is_score_decreasing())

    def test_score_decreasing_state_when_score_stays_same(self):
        """Test score decreasing state is False when score stays the same."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        tracker = ScoreTracker(patterns, default_score=0)

        # Decrease score first
        tracker.update("Twitter")
        self.assertEqual(tracker.get_score(), -5)
        self.assertTrue(tracker.is_score_decreasing())

        # Score stays the same (no match, default_score=0)
        tracker.update("Unknown Window")
        self.assertEqual(tracker.get_score(), -5)
        self.assertFalse(tracker.is_score_decreasing())

    def test_score_decreasing_state_continuous_decrease(self):
        """Test score decreasing state stays True during continuous decrease."""
        patterns = [{"regex": "twitter", "score": -5, "description": "Twitter"}]
        tracker = ScoreTracker(patterns, default_score=0)

        # First decrease
        tracker.update("Twitter")
        self.assertEqual(tracker.get_score(), -5)
        self.assertTrue(tracker.is_score_decreasing())

        # Second decrease
        tracker.update("Twitter")
        self.assertEqual(tracker.get_score(), -10)
        self.assertTrue(tracker.is_score_decreasing())

        # Third decrease
        tracker.update("Twitter")
        self.assertEqual(tracker.get_score(), -15)
        self.assertTrue(tracker.is_score_decreasing())

    def test_score_decreasing_state_with_default_score_negative(self):
        """Test score decreasing state with negative default_score."""
        patterns = [{"regex": "github", "score": 10, "description": "GitHub"}]
        tracker = ScoreTracker(patterns, default_score=-1)

        # Start with GitHub (score = 10)
        tracker.update("GitHub")
        self.assertEqual(tracker.get_score(), 10)
        self.assertFalse(tracker.is_score_decreasing())

        # Unknown window applies default_score=-1, decreasing score
        tracker.update("Unknown Window")
        self.assertEqual(tracker.get_score(), 9)
        self.assertTrue(tracker.is_score_decreasing())


if __name__ == "__main__":
    unittest.main()
