#!/usr/bin/env python3
"""Tests for score tracker module."""

import unittest
from pathlib import Path

try:
    from src.score_tracker import ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from score_tracker import ScoreTracker


class TestScoreTracker(unittest.TestCase):
    """Test cases for ScoreTracker class."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
            {"regex": "vscode", "score": 8, "description": "VS Code"},
        ]
        self.tracker = ScoreTracker(self.patterns, default_score=0)

    def test_initial_score(self):
        """Test initial score is zero."""
        self.assertEqual(self.tracker.get_score(), 0)

    def test_score_increase(self):
        """Test score increases when pattern matches."""
        score_changed, matched = self.tracker.update("GitHub - Pull Requests")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_score_decrease(self):
        """Test score decreases when negative pattern matches."""
        score_changed, matched = self.tracker.update("Twitter - Home")
        self.assertTrue(score_changed)
        self.assertEqual(self.tracker.get_score(), -5)

    def test_multiple_updates(self):
        """Test multiple score updates."""
        self.tracker.update("GitHub - Issues")
        self.assertEqual(self.tracker.get_score(), 10)

        self.tracker.update("VSCode Editor")
        self.assertEqual(self.tracker.get_score(), 18)  # vscode matches, +8

        self.tracker.update("Twitter Feed")
        self.assertEqual(self.tracker.get_score(), 13)  # twitter matches, -5

    def test_case_insensitive_matching(self):
        """Test regex matching is case insensitive."""
        self.tracker.update("GITHUB")
        self.assertEqual(self.tracker.get_score(), 10)

        self.tracker.update("GitHub")
        self.assertEqual(self.tracker.get_score(), 20)  # Still matches GitHub, +10

        self.tracker.update("github.com")
        self.assertEqual(self.tracker.get_score(), 30)  # Still matches GitHub, +10

    def test_no_match(self):
        """Test no score change when no pattern matches."""
        score_changed, matched = self.tracker.update("Random Window Title")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(self.tracker.get_score(), 0)

    def test_same_window_continuous_update(self):
        """Test score continues to change for same window title."""
        self.tracker.update("GitHub - Profile")
        self.assertEqual(self.tracker.get_score(), 10)

        # Same window, score should continue to increase
        score_changed, matched = self.tracker.update("GitHub - Profile")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 20)

    def test_first_pattern_wins(self):
        """Test only first matching pattern is applied."""
        patterns = [
            {"regex": "git", "score": 5, "description": "Git"},
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns)

        tracker.update("GitHub Repository")
        self.assertEqual(tracker.get_score(), 5)  # Matches "git" first

    def test_reset_score(self):
        """Test score reset functionality."""
        self.tracker.update("GitHub")
        self.assertEqual(self.tracker.get_score(), 10)

        self.tracker.reset_score()
        self.assertEqual(self.tracker.get_score(), 0)

    def test_get_current_match(self):
        """Test getting current matched pattern."""
        self.tracker.update("GitHub - Issues")
        matched = self.tracker.get_current_match()
        self.assertIsNotNone(matched)
        self.assertEqual(matched["description"], "GitHub")

    def test_regex_special_characters(self):
        """Test regex with special characters."""
        self.tracker.update("x.com - Home")
        self.assertEqual(self.tracker.get_score(), -5)

    def test_continuous_score_tracking(self):
        """Test score increases continuously while window remains active."""
        # Simulate being on GitHub for 5 updates (5 seconds)
        for i in range(1, 6):
            score_changed, matched = self.tracker.update("GitHub - Repository")
            self.assertTrue(score_changed)
            self.assertIsNotNone(matched)
            self.assertEqual(matched["description"], "GitHub")
            self.assertEqual(self.tracker.get_score(), 10 * i)

        # Switch to Twitter
        self.tracker.update("Twitter - Feed")
        self.assertEqual(self.tracker.get_score(), 45)  # 50 - 5

        # Stay on Twitter for 3 updates
        for i in range(2, 5):
            self.tracker.update("Twitter - Feed")
            expected_score = 50 - (5 * i)
            self.assertEqual(self.tracker.get_score(), expected_score)


class TestDefaultScore(unittest.TestCase):
    """Test cases for default_score functionality."""

    def test_default_score_zero_no_match(self):
        """Test default_score=0 does not change score when no pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=0)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), 0)

    def test_default_score_negative_no_match(self):
        """Test default_score with negative value applies when no pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertTrue(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), -1)

    def test_default_score_positive_no_match(self):
        """Test default_score with positive value applies when no pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=5)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertTrue(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), 5)

    def test_default_score_not_applied_when_pattern_matches(self):
        """Test default_score is NOT applied when a pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1)

        score_changed, matched = tracker.update("GitHub - Profile")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(tracker.get_score(), 10)  # Pattern score, not default

    def test_default_score_accumulates(self):
        """Test default_score accumulates over multiple updates."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-2)

        # No match 3 times
        tracker.update("Random Window 1")
        self.assertEqual(tracker.get_score(), -2)

        tracker.update("Random Window 2")
        self.assertEqual(tracker.get_score(), -4)

        tracker.update("Random Window 3")
        self.assertEqual(tracker.get_score(), -6)

    def test_default_score_mixed_with_pattern_matches(self):
        """Test default_score mixed with pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1)

        # Pattern match
        tracker.update("GitHub - Repository")
        self.assertEqual(tracker.get_score(), 10)

        # No match (default score)
        tracker.update("Random Window")
        self.assertEqual(tracker.get_score(), 9)  # 10 + (-1)

        # Pattern match again
        tracker.update("GitHub - Issues")
        self.assertEqual(tracker.get_score(), 19)  # 9 + 10

        # No match again
        tracker.update("Another Random Window")
        self.assertEqual(tracker.get_score(), 18)  # 19 + (-1)

    def test_default_score_helps_detect_misconfiguration(self):
        """Test default_score helps detect pattern misconfiguration."""
        # Simulate misconfigured patterns that never match
        patterns = [
            {"regex": "zzz_this_never_matches_zzz", "score": 10, "description": "Never"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1)

        # User browses various windows, but nothing matches
        for i in range(1, 6):
            tracker.update(f"Some Window {i}")
            # Score keeps decreasing, making it obvious patterns don't match
            self.assertEqual(tracker.get_score(), -i)


class TestApplyDefaultScoreMode(unittest.TestCase):
    """Test cases for apply_default_score_mode functionality."""

    def test_apply_default_score_mode_enabled_applies_default_score(self):
        """Test that default_score is applied when mode is enabled and no pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1, apply_default_score_mode=True)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertTrue(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), -1)

    def test_apply_default_score_mode_disabled_does_not_apply_default_score(self):
        """Test that default_score is NOT applied when mode is disabled."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1, apply_default_score_mode=False)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), 0)

    def test_apply_default_score_mode_disabled_no_score_accumulation(self):
        """Test that score does not accumulate when mode is disabled."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-2, apply_default_score_mode=False)

        # No match 3 times - score should stay 0
        tracker.update("Random Window 1")
        self.assertEqual(tracker.get_score(), 0)

        tracker.update("Random Window 2")
        self.assertEqual(tracker.get_score(), 0)

        tracker.update("Random Window 3")
        self.assertEqual(tracker.get_score(), 0)

    def test_apply_default_score_mode_enabled_accumulates_default_score(self):
        """Test that default_score accumulates when mode is enabled."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-2, apply_default_score_mode=True)

        # No match 3 times - score should accumulate
        tracker.update("Random Window 1")
        self.assertEqual(tracker.get_score(), -2)

        tracker.update("Random Window 2")
        self.assertEqual(tracker.get_score(), -4)

        tracker.update("Random Window 3")
        self.assertEqual(tracker.get_score(), -6)

    def test_apply_default_score_mode_disabled_with_pattern_matches(self):
        """Test that pattern matches still work when mode is disabled."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1, apply_default_score_mode=False)

        # Pattern match should still work
        tracker.update("GitHub - Repository")
        self.assertEqual(tracker.get_score(), 10)

        # No match - score should not change
        tracker.update("Random Window")
        self.assertEqual(tracker.get_score(), 10)

        # Pattern match again
        tracker.update("GitHub - Issues")
        self.assertEqual(tracker.get_score(), 20)

    def test_apply_default_score_mode_mixed_scenarios(self):
        """Test mixed scenarios with mode enabled and pattern matches."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1, apply_default_score_mode=True)

        # Pattern match
        tracker.update("GitHub - Repository")
        self.assertEqual(tracker.get_score(), 10)

        # No match (default score applied)
        tracker.update("Random Window")
        self.assertEqual(tracker.get_score(), 9)

        # Pattern match again
        tracker.update("GitHub - Issues")
        self.assertEqual(tracker.get_score(), 19)

    def test_apply_default_score_mode_disabled_with_positive_default_score(self):
        """Test that positive default_score is also not applied when mode is disabled."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=5, apply_default_score_mode=False)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), 0)

    def test_apply_default_score_mode_disabled_with_zero_default_score(self):
        """Test mode disabled with default_score=0 (both mechanisms for no change)."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=0, apply_default_score_mode=False)

        score_changed, matched = tracker.update("Random Window Title")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), 0)

    def test_apply_default_score_mode_update_config(self):
        """Test that update_config changes apply_default_score_mode."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1, apply_default_score_mode=True)

        # Initially mode is enabled - default score applies
        score_changed, matched = tracker.update("Random Window")
        self.assertTrue(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), -1)

        # Update config to disable mode
        tracker.update_config(patterns, default_score=-1, apply_default_score_mode=False)

        # Now default score should not apply - using same window title
        score_changed, matched = tracker.update("Random Window")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), -1)  # Score unchanged


if __name__ == "__main__":
    unittest.main()
