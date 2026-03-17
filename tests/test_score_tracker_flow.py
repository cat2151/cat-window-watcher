#!/usr/bin/env python3
"""Tests for score tracker module - flow state tracking."""

import unittest
from pathlib import Path

try:
    from src.score_tracker import ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from score_tracker import ScoreTracker


class TestFlowStateTracking(unittest.TestCase):
    """Test cases for flow state tracking functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
        ]

    def test_initial_flow_state(self):
        """Test that flow state is initially false."""
        tracker = ScoreTracker(self.patterns, default_score=0)
        self.assertFalse(tracker.is_in_flow_state())
        self.assertEqual(tracker.get_flow_state_duration(), 0.0)

    def test_flow_state_enters_on_score_increase(self):
        """Test that flow state becomes true when score increases."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # Score increases
        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())
        self.assertGreaterEqual(tracker.get_flow_state_duration(), 0.0)

    def test_flow_state_stays_when_score_stays_same(self):
        """Test that flow state remains when score stays the same."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # First increase
        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())

        # Score stays same (no match, default_score=0)
        tracker.update("Random Window")
        self.assertTrue(tracker.is_in_flow_state())

    def test_flow_state_does_not_enter_when_score_stays_zero(self):
        """Test that flow state does not enter when score stays at zero."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # No match, score stays at 0
        tracker.update("Random Window 1")
        self.assertFalse(tracker.is_in_flow_state())

        # Another no match, score still stays at 0
        tracker.update("Random Window 2")
        self.assertFalse(tracker.is_in_flow_state())

    def test_flow_state_exits_on_score_decrease(self):
        """Test that flow state becomes false when score decreases."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # Score increases
        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())

        # Score decreases
        tracker.update("Twitter Feed")
        self.assertFalse(tracker.is_in_flow_state())
        self.assertEqual(tracker.get_flow_state_duration(), 0.0)

    def test_flow_state_transitions_from_negative_to_positive(self):
        """Test flow state transition from negative score change to positive."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # Start with negative score
        tracker.update("Twitter Feed")
        self.assertFalse(tracker.is_in_flow_state())

        # Transition to positive
        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())

    def test_flow_state_duration_increases_over_time(self):
        """Test that flow state duration increases while in flow state."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(self.patterns, default_score=0)

        # Enter flow state
        start_time = datetime(2024, 1, 1, 10, 0, 0)
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = start_time
            tracker.update("GitHub")
            self.assertTrue(tracker.is_in_flow_state())

        # Check duration after 5 seconds
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 5)
            duration = tracker.get_flow_state_duration()
            self.assertAlmostEqual(duration, 5.0, delta=0.1)

        # Check duration after 10 seconds
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            duration = tracker.get_flow_state_duration()
            self.assertAlmostEqual(duration, 10.0, delta=0.1)

    def test_flow_state_resets_on_exit(self):
        """Test that flow state duration resets when exiting flow state."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(self.patterns, default_score=0)

        # Enter flow state and wait
        start_time = datetime(2024, 1, 1, 10, 0, 0)
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = start_time
            tracker.update("GitHub")
            self.assertTrue(tracker.is_in_flow_state())

        # Wait 10 seconds
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            duration = tracker.get_flow_state_duration()
            self.assertAlmostEqual(duration, 10.0, delta=0.1)

        # Exit flow state
        tracker.update("Twitter Feed")
        self.assertFalse(tracker.is_in_flow_state())
        self.assertEqual(tracker.get_flow_state_duration(), 0.0)

    def test_flow_state_restarts_on_reentry(self):
        """Test that flow state duration restarts when re-entering flow state."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(self.patterns, default_score=0)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker.update("GitHub")
            self.assertTrue(tracker.is_in_flow_state())

        # Wait 10 seconds
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            self.assertAlmostEqual(tracker.get_flow_state_duration(), 10.0, delta=0.1)

        # Exit flow state
        tracker.update("Twitter Feed")
        self.assertFalse(tracker.is_in_flow_state())

        # Re-enter flow state (should restart timer)
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 15)
            tracker.update("GitHub")
            self.assertTrue(tracker.is_in_flow_state())

        # Check duration is from new start time
        with patch("src.score_tracker.datetime") as mock_datetime_class:
            mock_datetime_class.now.return_value = datetime(2024, 1, 1, 10, 0, 20)
            duration = tracker.get_flow_state_duration()
            self.assertAlmostEqual(duration, 5.0, delta=0.1)

    def test_flow_state_with_default_score_positive(self):
        """Test flow state with positive default score."""
        tracker = ScoreTracker(self.patterns, default_score=1)

        # No match but default score is positive, so score increases
        tracker.update("Random Window")
        self.assertTrue(tracker.is_in_flow_state())

    def test_flow_state_with_default_score_negative(self):
        """Test flow state with negative default score."""
        tracker = ScoreTracker(self.patterns, default_score=-1)

        # No match and default score is negative, so score decreases
        tracker.update("Random Window")
        self.assertFalse(tracker.is_in_flow_state())

    def test_flow_state_continuous_positive_scores(self):
        """Test flow state remains active during continuous positive scores."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # Multiple positive updates
        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())

        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())

        tracker.update("GitHub")
        self.assertTrue(tracker.is_in_flow_state())

    def test_get_flow_mode_elapsed_seconds_in_flow_state(self):
        """Test get_flow_mode_elapsed_seconds returns correct value in flow state."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(self.patterns, default_score=0)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker.update("GitHub")

        # Check elapsed seconds after 25 seconds
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 25)
            elapsed = tracker.get_flow_mode_elapsed_seconds()
            self.assertEqual(elapsed, 25)

    def test_get_flow_mode_elapsed_seconds_not_in_flow_state(self):
        """Test get_flow_mode_elapsed_seconds returns 0 when not in flow state."""
        tracker = ScoreTracker(self.patterns, default_score=0)

        # Not in flow state initially
        elapsed = tracker.get_flow_mode_elapsed_seconds()
        self.assertEqual(elapsed, 0)

        # After decreasing score (not in flow state)
        tracker.update("Twitter Feed")
        elapsed = tracker.get_flow_mode_elapsed_seconds()
        self.assertEqual(elapsed, 0)


if __name__ == "__main__":
    unittest.main()
