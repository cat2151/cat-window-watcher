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


class TestGitHubWindowTitlePatterns(unittest.TestCase):
    """Test cases specifically for GitHub window title pattern matching.

    Tests the improved regex pattern that matches both:
    1. Traditional "github" embedded in titles
    2. GitHub page format: "Content · owner/repo · GitHub"
    """

    def setUp(self):
        """Set up test fixtures with improved GitHub pattern."""
        self.patterns = [
            {
                "regex": "github|· GitHub$",
                "score": 10,
                "description": "GitHub",
            },
        ]
        self.tracker = ScoreTracker(self.patterns, default_score=0)

    def test_traditional_github_lowercase(self):
        """Test matching traditional github.com URLs."""
        score_changed, matched = self.tracker.update("github.com")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["description"], "GitHub")
        self.assertEqual(self.tracker.get_score(), 10)

    def test_traditional_github_mixed_case(self):
        """Test matching GitHub with mixed case."""
        score_changed, matched = self.tracker.update("GitHub - Profile")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_pull_requests_page(self):
        """Test matching 'Pull requests · owner/repo · GitHub' format."""
        score_changed, matched = self.tracker.update("Pull requests · cat2151/cat-window-watcher · GitHub")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(matched["description"], "GitHub")
        self.assertEqual(self.tracker.get_score(), 10)

    def test_code_page(self):
        """Test matching 'Code · owner/repo · GitHub' format."""
        score_changed, matched = self.tracker.update("Code · microsoft/vscode · GitHub")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_issues_page(self):
        """Test matching 'Issues · owner/repo · GitHub' format."""
        score_changed, matched = self.tracker.update("Issues · facebook/react · GitHub")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_repo_at_branch_format(self):
        """Test matching 'owner/repo at branch · GitHub' format."""
        score_changed, matched = self.tracker.update("cat2151/cat-window-watcher at main · GitHub")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_actions_page(self):
        """Test matching 'Actions · owner/repo · GitHub' format."""
        score_changed, matched = self.tracker.update("Actions · torvalds/linux · GitHub")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_specific_pr_title(self):
        """Test matching specific PR title format."""
        score_changed, matched = self.tracker.update(
            "Add login feature · Pull Request #42 · octocat/Hello-World · GitHub"
        )
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_file_path_format(self):
        """Test matching file path format."""
        score_changed, matched = self.tracker.update("src/utils/helpers.js at main · octocat/Hello-World · GitHub")
        self.assertTrue(score_changed)
        self.assertIsNotNone(matched)
        self.assertEqual(self.tracker.get_score(), 10)

    def test_non_github_not_matched(self):
        """Test that non-GitHub pages are not matched."""
        score_changed, matched = self.tracker.update("Random Window Title")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(self.tracker.get_score(), 0)

    def test_non_github_ending_pattern(self):
        """Test that other sites with similar ending don't match."""
        # This should NOT match because it doesn't end with "· GitHub"
        score_changed, matched = self.tracker.update("Some Page · Other Site")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(self.tracker.get_score(), 0)

    def test_multiple_github_pages_accumulate_score(self):
        """Test that browsing multiple GitHub pages accumulates score."""
        self.tracker.update("Pull requests · cat2151/cat-window-watcher · GitHub")
        self.assertEqual(self.tracker.get_score(), 10)

        self.tracker.update("Code · microsoft/vscode · GitHub")
        self.assertEqual(self.tracker.get_score(), 20)

        self.tracker.update("github.com")
        self.assertEqual(self.tracker.get_score(), 30)


class TestConfigUpdate(unittest.TestCase):
    """Test cases for ScoreTracker configuration updates."""

    def test_update_config_changes_patterns(self):
        """Test that update_config changes window patterns."""
        initial_patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(initial_patterns, default_score=0)

        # Test with initial pattern
        tracker.update("GitHub - Profile")
        self.assertEqual(tracker.get_score(), 10)

        # Update configuration with new patterns
        new_patterns = [
            {"regex": "twitter", "score": -5, "description": "Twitter"},
            {"regex": "facebook", "score": -3, "description": "Facebook"},
        ]
        tracker.update_config(new_patterns, 0)

        # Old pattern should no longer match
        score_changed, matched = tracker.update("GitHub - Profile")
        self.assertFalse(score_changed)
        self.assertIsNone(matched)
        self.assertEqual(tracker.get_score(), 10)  # Score unchanged

        # New pattern should match
        tracker.update("Twitter - Feed")
        self.assertEqual(tracker.get_score(), 5)  # 10 + (-5)

    def test_update_config_changes_default_score(self):
        """Test that update_config changes default_score."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=-1)

        # Test with initial default score
        tracker.update("Random Window")
        self.assertEqual(tracker.get_score(), -1)

        # Update configuration with new default score
        tracker.update_config(patterns, 5)

        # New default score should apply
        tracker.update("Another Random Window")
        self.assertEqual(tracker.get_score(), 4)  # -1 + 5

    def test_update_config_preserves_score(self):
        """Test that update_config preserves accumulated score."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=0)

        # Accumulate some score
        tracker.update("GitHub - Profile")
        tracker.update("GitHub - Issues")
        self.assertEqual(tracker.get_score(), 20)

        # Update configuration
        new_patterns = [
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        tracker.update_config(new_patterns, 0)

        # Score should be preserved
        self.assertEqual(tracker.get_score(), 20)

    def test_update_config_applies_immediately(self):
        """Test that updated config applies immediately on next update."""
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
        ]
        tracker = ScoreTracker(patterns, default_score=0)

        # Update configuration
        new_patterns = [
            {"regex": "vscode", "score": 15, "description": "VS Code"},
        ]
        tracker.update_config(new_patterns, -2)

        # New pattern should apply immediately
        tracker.update("VSCode - Editor")
        self.assertEqual(tracker.get_score(), 15)

        # New default score should apply immediately
        tracker.update("Random Window")
        self.assertEqual(tracker.get_score(), 13)  # 15 + (-2)


class TestMildPenaltyMode(unittest.TestCase):
    """Test cases for mild penalty mode functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter|x\\.com", "score": -5, "description": "Twitter/X"},
            {"regex": "youtube", "score": -7, "description": "YouTube"},
        ]

    def test_mild_penalty_mode_disabled(self):
        """Test that mild penalty mode does not affect scores when disabled."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=False,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        # Negative scores should apply normally
        tracker.update("Twitter Feed")
        self.assertEqual(tracker.get_score(), -5)

        tracker.update("YouTube Video")
        self.assertEqual(tracker.get_score(), -12)  # -5 + (-7)

    def test_mild_penalty_mode_enabled_during_hours(self):
        """Test that mild penalty mode limits negative scores to -1 during specified hours."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        # Mock datetime to return hour 22 (within mild penalty hours)
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 30)  # 22:30

            # Negative scores should be limited to -1
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -1)

            tracker.update("YouTube Video")
            self.assertEqual(tracker.get_score(), -2)  # -1 + (-1)

            # Positive scores should not be affected
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 8)  # -2 + 10

    def test_mild_penalty_mode_outside_hours(self):
        """Test that mild penalty mode does not affect scores outside specified hours."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        # Mock datetime to return hour 10 (outside mild penalty hours)
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0)  # 10:00

            # Negative scores should apply normally
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -5)

            tracker.update("YouTube Video")
            self.assertEqual(tracker.get_score(), -12)  # -5 + (-7)

    def test_mild_penalty_mode_with_default_score(self):
        """Test that mild penalty mode applies to default score during specified hours."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=-3,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        # Mock datetime to return hour 22
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 0)  # 22:00

            # Default score should be limited to -1
            tracker.update("Random Window")
            self.assertEqual(tracker.get_score(), -1)

            tracker.update("Another Random Window")
            self.assertEqual(tracker.get_score(), -2)  # -1 + (-1)

    def test_mild_penalty_mode_time_range_boundaries(self):
        """Test mild penalty mode at time range boundaries."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        # Test at start hour (22:00) - should apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 0)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -1)

        # Test at end hour (23:59) - should apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 23, 59)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -1)

        # Test just before start hour (21:59) - should not apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 21, 59)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -5)

        # Test just after end hour (00:00 next day) - should not apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 2, 0, 0)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -5)

    def test_mild_penalty_mode_wrapped_time_range(self):
        """Test mild penalty mode with time range that wraps around midnight."""
        from datetime import datetime
        from unittest.mock import patch

        # Time range: 23:00 - 01:00 (wraps around midnight)
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=True,
            mild_penalty_start_hour=23,
            mild_penalty_end_hour=1,
        )

        # Test at 23:30 - should apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 23, 30)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -1)

        # Test at 00:30 - should apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 2, 0, 30)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -1)

        # Test at 01:00 - should apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 2, 1, 0)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -1)

        # Test at 02:00 - should not apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 2, 2, 0)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -5)

        # Test at 22:00 - should not apply mild penalty
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 0)
            tracker.reset_score()
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -5)

    def test_mild_penalty_mode_update_config(self):
        """Test that update_config changes mild penalty mode settings."""
        tracker = ScoreTracker(
            self.patterns,
            default_score=-1,
            mild_penalty_mode=False,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        from datetime import datetime
        from unittest.mock import patch

        # Mock datetime to return hour 22
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 30)

            # Initially, mild penalty mode is disabled
            tracker.update("Twitter Feed")
            self.assertEqual(tracker.get_score(), -5)

            # Update config to enable mild penalty mode
            tracker.update_config(
                self.patterns,
                default_score=-1,
                mild_penalty_mode=True,
                mild_penalty_start_hour=22,
                mild_penalty_end_hour=23,
            )

            # Now mild penalty should apply
            tracker.update("YouTube Video")
            self.assertEqual(tracker.get_score(), -6)  # -5 + (-1)

    def test_mild_penalty_mode_does_not_affect_positive_scores(self):
        """Test that mild penalty mode only affects negative scores."""
        from datetime import datetime
        from unittest.mock import patch

        tracker = ScoreTracker(
            self.patterns,
            default_score=5,
            mild_penalty_mode=True,
            mild_penalty_start_hour=22,
            mild_penalty_end_hour=23,
        )

        # Mock datetime to return hour 22
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 22, 30)

            # Positive scores should not be affected
            tracker.update("GitHub")
            self.assertEqual(tracker.get_score(), 10)

            # Positive default score should not be affected
            tracker.update("Random Window")
            self.assertEqual(tracker.get_score(), 15)  # 10 + 5


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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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
        with patch("src.score_tracker.datetime") as mock_datetime:
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

        with patch("src.score_tracker.datetime") as mock_datetime:
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

        with patch("src.score_tracker.datetime") as mock_datetime:
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


if __name__ == "__main__":
    unittest.main()
