#!/usr/bin/env python3
"""Tests for score tracker module - self-window score and elapsed seconds tracking."""

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


class TestSelfWindowScore(unittest.TestCase):
    """Test cases for self-window score functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
        ]
        self.self_window_title = "Cat Window Watcher - Cat is watching you -"

    def test_self_window_score_zero(self):
        """Test that self_window_score=0 doesn't change score."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=0,
            self_window_title=self.self_window_title,
        )

        score_changed, matched = tracker.update(self.self_window_title)
        self.assertFalse(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["description"], "Cat Window Watcher (self)")
        self.assertEqual(tracker.get_score(), 0)

    def test_self_window_score_positive(self):
        """Test that positive self_window_score increases score."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=3,
            self_window_title=self.self_window_title,
        )

        score_changed, matched = tracker.update(self.self_window_title)
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["description"], "Cat Window Watcher (self)")
        self.assertEqual(tracker.get_score(), 3)

    def test_self_window_score_negative(self):
        """Test that negative self_window_score decreases score."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=-2,
            self_window_title=self.self_window_title,
        )

        score_changed, matched = tracker.update(self.self_window_title)
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["description"], "Cat Window Watcher (self)")
        self.assertEqual(tracker.get_score(), -2)

    def test_self_window_not_apply_default_score(self):
        """Test that default_score is NOT applied for self window."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            apply_default_score_mode=True,
            self_window_score=0,
            self_window_title=self.self_window_title,
        )

        # Self window should not apply default_score even when it's enabled
        score_changed, matched = tracker.update(self.self_window_title)
        self.assertFalse(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(tracker.get_score(), 0)

    def test_self_window_accumulates_score(self):
        """Test that self_window_score accumulates over multiple updates."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=2,
            self_window_title=self.self_window_title,
        )

        # First update
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 2)

        # Second update
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 4)

        # Third update
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 6)

    def test_self_window_mixed_with_other_windows(self):
        """Test self_window_score mixed with pattern matches."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=1,
            self_window_title=self.self_window_title,
        )

        # Pattern match
        tracker.update("GitHub - Repository")
        self.assertEqual(tracker.get_score(), 10)

        # Self window
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 11)

        # Another pattern match
        tracker.update("Twitter Feed")
        self.assertEqual(tracker.get_score(), 6)

        # Self window again
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 7)

    def test_self_window_prevents_pattern_matching(self):
        """Test that self window is checked before pattern matching."""
        # Create pattern that would match the window title
        patterns = [
            {"regex": "Cat.*Watcher", "score": 10, "description": "Should not match"},
        ]
        tracker = ScoreTracker(
            patterns,
            default_score=-1,
            self_window_score=5,
            self_window_title=self.self_window_title,
        )

        score_changed, matched = tracker.update(self.self_window_title)
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        # Should match as self window, not the pattern
        self.assertEqual(matched["description"], "Cat Window Watcher (self)")
        self.assertEqual(tracker.get_score(), 5)

    def test_self_window_with_empty_title(self):
        """Test that empty self_window_title disables the feature."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=5,
            self_window_title="",
        )

        # Should apply default_score since self window matching is disabled
        score_changed, matched = tracker.update(self.self_window_title)
        self.assertTrue(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), -1)

    def test_self_window_exact_match_only(self):
        """Test that self window requires exact match."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=5,
            self_window_title=self.self_window_title,
        )

        # Partial match should not trigger self window
        score_changed, matched = tracker.update("Cat Window Watcher")
        self.assertTrue(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), -1)

    def test_self_window_update_config(self):
        """Test that update_config changes self_window_score."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=2,
            self_window_title=self.self_window_title,
        )

        # Test with initial self_window_score
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 2)

        # Update configuration with new self_window_score
        tracker.update_config(
            self.patterns,
            default_score=-1,
            self_window_score=5,
            self_window_title=self.self_window_title,
        )

        # New self_window_score should apply
        tracker.update(self.self_window_title)
        self.assertEqual(tracker.get_score(), 7)  # 2 + 5

    def test_self_window_update_config_change_title(self):
        """Test that update_config can change self_window_title."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            self_window_score=3,
            self_window_title="Old Title",
        )

        # Test with old title
        tracker.update("Old Title")
        self.assertEqual(tracker.get_score(), 3)

        # Update configuration with new title
        tracker.update_config(
            self.patterns,
            default_score=-1,
            self_window_score=3,
            self_window_title="New Title",
        )

        # Old title should no longer match as self window
        tracker.update("Old Title")
        self.assertEqual(tracker.get_score(), 2)  # 3 + (-1) default_score

        # New title should match as self window
        tracker.update("New Title")
        self.assertEqual(tracker.get_score(), 5)  # 2 + 3

    def test_self_window_score_with_mild_penalty_mode(self):
        """Test that self_window_score is affected by mild penalty mode."""
        from datetime import datetime
        from unittest.mock import patch

        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(
            patterns,
            default_score=-1,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
            self_window_score=-5,
            self_window_title=self.self_window_title,
        )

        # Mock datetime to return hour 22 (within mild penalty hours)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 30)  # 22:30

            # Negative self_window_score should be limited to -1
            tracker.update(self.self_window_title)
            self.assertEqual(tracker.get_score(), -1)

            # Second update should also be limited to -1
            tracker.update(self.self_window_title)
            self.assertEqual(tracker.get_score(), -2)  # -1 + (-1)

        # Mock datetime to return hour 10 (outside mild penalty hours)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0)  # 10:00

            tracker.reset_score()

            # Negative self_window_score should apply normally
            tracker.update(self.self_window_title)
            self.assertEqual(tracker.get_score(), -5)

    def test_self_window_score_positive_not_affected_by_mild_penalty(self):
        """Test that positive self_window_score is not affected by mild penalty mode."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
            self_window_score=5,
            self_window_title=self.self_window_title,
        )

        # Mock datetime to return hour 22 (within mild penalty hours)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 30)

            # Positive self_window_score should not be affected by mild penalty
            tracker.update(self.self_window_title)
            self.assertEqual(tracker.get_score(), 5)


class TestElapsedSecondsTracking(unittest.TestCase):
    """Test cases for elapsed seconds since window became active."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
        ]

    def test_initial_elapsed_seconds(self):
        """Test that elapsed seconds is 0 initially."""
        from datetime import datetime
        from unittest.mock import patch

        # Mock datetime in src.score_tracker so that initialization time and
        # elapsed-time calculation use the same fixed timestamp.
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker = ScoreTracker(self.patterns, default_score=0)
            elapsed = tracker.get_current_window_elapsed_seconds()
        self.assertEqual(elapsed, 0)

    def test_elapsed_seconds_increases_with_time(self):
        """Test that elapsed seconds increases over time for same window."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = None

        # Start with GitHub window; initialize tracker under mocked datetime
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker = ScoreTracker(self.patterns, default_score=0)
            tracker.update("GitHub - Repository")

        # Check elapsed after 5 seconds
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 5)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 5)

        # Check elapsed after 30 seconds
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 30)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 30)

    def test_elapsed_seconds_resets_on_window_change(self):
        """Test that elapsed seconds resets when window title changes."""
        from datetime import datetime
        from unittest.mock import patch

        # Initialize tracker and start with GitHub window at 10:00:00
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker = ScoreTracker(self.patterns, default_score=0)
            tracker.update("GitHub - Repository")

        # Check elapsed after 10 seconds (at 10:00:10)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 10)

        # Change to Twitter window at 10:00:15
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 15)
            tracker.update("Twitter - Feed")

        # Elapsed should reset and be close to 0
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 15)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 0)

        # Check elapsed for new window after 7 seconds (at 10:00:22)
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 22)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 7)

    def test_elapsed_seconds_continues_on_same_window(self):
        """Test that elapsed seconds continues to increase for same window title."""
        from datetime import datetime
        from unittest.mock import patch

        # Start with GitHub window at 10:00:00
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker = ScoreTracker(self.patterns, default_score=0)
            tracker.update("GitHub - Repository")

        # Same window at 10:00:05
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 5)
            tracker.update("GitHub - Repository")
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 5)

        # Same window again at 10:00:10
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            tracker.update("GitHub - Repository")
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 10)

    def test_elapsed_seconds_different_windows_with_same_pattern(self):
        """Test that elapsed seconds resets when window title changes even if same pattern matches."""
        from datetime import datetime
        from unittest.mock import patch

        # Start with GitHub Repository at 10:00:00
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            tracker = ScoreTracker(self.patterns, default_score=0)
            tracker.update("GitHub - Repository")

        # Check elapsed after 10 seconds
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 10)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 10)

        # Change to GitHub Issues (different window, same pattern) at 10:00:15
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 15)
            tracker.update("GitHub - Issues")

        # Elapsed should reset even though pattern is the same
        with patch(_SCORE_TRACKER_DATETIME_PATH) as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 15)
            elapsed = tracker.get_current_window_elapsed_seconds()
            self.assertEqual(elapsed, 0)


if __name__ == "__main__":
    unittest.main()
