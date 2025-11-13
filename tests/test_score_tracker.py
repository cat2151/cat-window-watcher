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
        self.tracker = ScoreTracker(self.patterns)

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


if __name__ == "__main__":
    unittest.main()
