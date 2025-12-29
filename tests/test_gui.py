#!/usr/bin/env python3
"""Tests for GUI module proximity detection."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

try:
    from src.config import Config
    from src.score_tracker import ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config
    from score_tracker import ScoreTracker


class MockScoreDisplay:
    """Mock ScoreDisplay class for testing proximity detection logic."""

    def __init__(self, score_tracker, config):
        self.score_tracker = score_tracker
        self.config = config
        self._mouse_in_proximity = False
        self.root = MagicMock()

    def _is_mouse_in_proximity(self):
        """Check if mouse is within proximity distance of the window."""
        # Get mouse position relative to screen
        mouse_x = self.root.winfo_pointerx()
        mouse_y = self.root.winfo_pointery()

        # Get window position and dimensions
        window_x = self.root.winfo_x()
        window_y = self.root.winfo_y()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Get proximity distance from config
        proximity_distance = self.config.get_proximity_distance()

        # Calculate if mouse is within proximity distance
        # Check if mouse is within the expanded bounding box
        in_proximity = (
            mouse_x >= window_x - proximity_distance
            and mouse_x <= window_x + window_width + proximity_distance
            and mouse_y >= window_y - proximity_distance
            and mouse_y <= window_y + window_height + proximity_distance
        )

        return in_proximity

    def _update_proximity_based_topmost(self):
        """Update window topmost state based on mouse proximity."""
        # Only apply proximity-based behavior if both settings are enabled
        if not self.config.get_always_on_top() or not self.config.get_hide_on_mouse_proximity():
            return

        # Check if mouse is in proximity
        mouse_in_proximity = self._is_mouse_in_proximity()

        # Update topmost state if proximity state changed
        if mouse_in_proximity != self._mouse_in_proximity:
            self._mouse_in_proximity = mouse_in_proximity

            # If mouse is in proximity, remove topmost (send to back)
            # If mouse is away, set topmost (bring to front)
            self.root.attributes("-topmost", not mouse_in_proximity)


class TestGuiProximity(unittest.TestCase):
    """Test cases for GUI proximity detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def _create_mock_gui(self, config_content):
        """Create a mock GUI with given configuration."""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))
        score_tracker = ScoreTracker(config.get_window_patterns(), config.get_default_score())
        gui = MockScoreDisplay(score_tracker, config)
        return gui, gui.root

    def test_is_mouse_in_proximity_within_distance(self):
        """Test proximity detection when mouse is within distance."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse at (80, 120) - 20 pixels to the left of window (within 50px)
        mock_root.winfo_pointerx.return_value = 80
        mock_root.winfo_pointery.return_value = 120

        result = gui._is_mouse_in_proximity()
        self.assertTrue(result)

    def test_is_mouse_in_proximity_outside_distance(self):
        """Test proximity detection when mouse is outside distance."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse at (20, 120) - 80 pixels to the left of window (outside 50px)
        mock_root.winfo_pointerx.return_value = 20
        mock_root.winfo_pointery.return_value = 120

        result = gui._is_mouse_in_proximity()
        self.assertFalse(result)

    def test_is_mouse_in_proximity_inside_window(self):
        """Test proximity detection when mouse is inside window."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse at (250, 150) - inside window
        mock_root.winfo_pointerx.return_value = 250
        mock_root.winfo_pointery.return_value = 150

        result = gui._is_mouse_in_proximity()
        self.assertTrue(result)

    def test_update_proximity_based_topmost_feature_disabled(self):
        """Test that proximity update does nothing when feature is disabled."""
        config_content = """
always_on_top = false
hide_on_mouse_proximity = false
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse within proximity
        mock_root.winfo_pointerx.return_value = 80
        mock_root.winfo_pointery.return_value = 120

        # Call update
        gui._update_proximity_based_topmost()

        # Should not call attributes (feature disabled)
        mock_root.attributes.assert_not_called()

    def test_update_proximity_based_topmost_mouse_enters_proximity(self):
        """Test window moves to background when mouse enters proximity."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Initially mouse is far away
        gui._mouse_in_proximity = False

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse enters proximity
        mock_root.winfo_pointerx.return_value = 80
        mock_root.winfo_pointery.return_value = 120

        # Call update
        gui._update_proximity_based_topmost()

        # Should set topmost to False (move to background)
        mock_root.attributes.assert_called_with("-topmost", False)
        self.assertTrue(gui._mouse_in_proximity)

    def test_update_proximity_based_topmost_mouse_leaves_proximity(self):
        """Test window returns to foreground when mouse leaves proximity."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Initially mouse is in proximity
        gui._mouse_in_proximity = True

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse leaves proximity
        mock_root.winfo_pointerx.return_value = 20
        mock_root.winfo_pointery.return_value = 120

        # Call update
        gui._update_proximity_based_topmost()

        # Should set topmost to True (return to foreground)
        mock_root.attributes.assert_called_with("-topmost", True)
        self.assertFalse(gui._mouse_in_proximity)

    def test_update_proximity_based_topmost_no_state_change(self):
        """Test that topmost is not updated when proximity state doesn't change."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Initially mouse is in proximity
        gui._mouse_in_proximity = True

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse still in proximity
        mock_root.winfo_pointerx.return_value = 80
        mock_root.winfo_pointery.return_value = 120

        # Call update
        gui._update_proximity_based_topmost()

        # Should not call attributes (no state change)
        mock_root.attributes.assert_not_called()

    def test_proximity_distance_zero(self):
        """Test proximity detection with distance set to zero."""
        config_content = """
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 0

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Window at (100, 100) with size 400x200
        mock_root.winfo_x.return_value = 100
        mock_root.winfo_y.return_value = 100
        mock_root.winfo_width.return_value = 400
        mock_root.winfo_height.return_value = 200

        # Mouse at edge of window (exactly at boundary)
        mock_root.winfo_pointerx.return_value = 100
        mock_root.winfo_pointery.return_value = 100

        result = gui._is_mouse_in_proximity()
        self.assertTrue(result)

        # Mouse 1 pixel outside window
        mock_root.winfo_pointerx.return_value = 99
        mock_root.winfo_pointery.return_value = 100

        result = gui._is_mouse_in_proximity()
        self.assertFalse(result)


class MockScoreDisplayWithColorTracking(MockScoreDisplay):
    """Extended mock for testing score color changes."""

    def __init__(self, score_tracker, window_monitor, config):
        super().__init__(score_tracker, config)
        self.window_monitor = window_monitor
        self._previous_score = score_tracker.get_score()
        self.score_label = MagicMock()

    def update_display_color_logic(self, window_title):
        """Simulate the color update logic from update_display."""
        # Update score
        self.score_tracker.update(window_title)

        # Get current score
        current_score = self.score_tracker.get_score()

        # Update score color based on score change
        if current_score < self._previous_score:
            # Score decreased - use score_down_color
            score_color = self.config.get_score_down_color()
        else:
            # Score increased or stayed the same - use score_up_color
            score_color = self.config.get_score_up_color()

        self.score_label.config(fg=score_color)
        self._previous_score = current_score

        return score_color


class TestGuiScoreColors(unittest.TestCase):
    """Test cases for GUI score color switching."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_mock_gui(self, config_content):
        """Create a mock GUI with given configuration."""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))
        score_tracker = ScoreTracker(config.get_window_patterns(), config.get_default_score())
        window_monitor = MagicMock()
        gui = MockScoreDisplayWithColorTracking(score_tracker, window_monitor, config)
        return gui

    def test_score_color_increases_uses_up_color(self):
        """Test that score increase uses score_up_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Trigger score increase
        color = gui.update_display_color_logic("github.com")

        # Verify score_up_color is used
        self.assertEqual(color, "#00ff00")
        gui.score_label.config.assert_called_with(fg="#00ff00")

    def test_score_color_decreases_uses_down_color(self):
        """Test that score decrease uses score_down_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -15
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # First increase score
        gui.update_display_color_logic("github.com")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score
        color = gui.update_display_color_logic("twitter.com")

        # Verify score_down_color is used
        self.assertEqual(color, "#ff0000")
        self.assertEqual(gui.score_tracker.get_score(), -5)

    def test_score_color_stays_same_uses_up_color(self):
        """Test that no score change uses score_up_color."""
        config_content = """
score_up_color = "#ffffff"
score_down_color = "#ff0000"
default_score = 0
apply_default_score_mode = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # First increase score
        gui.update_display_color_logic("github.com")

        # Window that doesn't match any pattern (score stays same)
        color = gui.update_display_color_logic("random window")

        # Verify score_up_color is used (score didn't decrease)
        self.assertEqual(color, "#ffffff")

    def test_score_color_multiple_increases(self):
        """Test multiple consecutive score increases use score_up_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 5
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Multiple increases
        for _ in range(3):
            color = gui.update_display_color_logic("github.com")
            self.assertEqual(color, "#00ff00")

        # Final score should be 15
        self.assertEqual(gui.score_tracker.get_score(), 15)

    def test_score_color_multiple_decreases(self):
        """Test multiple consecutive score decreases use score_down_color."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Multiple decreases
        for _ in range(3):
            color = gui.update_display_color_logic("twitter.com")
            self.assertEqual(color, "#ff0000")

        # Final score should be -15
        self.assertEqual(gui.score_tracker.get_score(), -15)

    def test_score_color_alternating_changes(self):
        """Test alternating score increases and decreases use correct colors."""
        config_content = """
score_up_color = "#00ff00"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Increase
        color = gui.update_display_color_logic("github.com")
        self.assertEqual(color, "#00ff00")

        # Decrease
        color = gui.update_display_color_logic("twitter.com")
        self.assertEqual(color, "#ff0000")

        # Increase again
        color = gui.update_display_color_logic("github.com")
        self.assertEqual(color, "#00ff00")

        # Decrease again
        color = gui.update_display_color_logic("twitter.com")
        self.assertEqual(color, "#ff0000")

    def test_score_color_initial_state_uses_up_color(self):
        """Test that initial state (score 0) uses score_up_color."""
        config_content = """
score_up_color = "#ffffff"
score_down_color = "#ff0000"

[[window_patterns]]
regex = "test"
score = 1
description = "Test"
"""
        gui = self._create_mock_gui(config_content)

        # Initial score is 0, check that previous score is initialized correctly
        self.assertEqual(gui._previous_score, 0)

    def test_score_color_with_default_colors(self):
        """Test score color switching with default color values."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -15
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Increase - should use default #ffffff
        color = gui.update_display_color_logic("github.com")
        self.assertEqual(color, "#ffffff")

        # Decrease - should use default #ff0000
        color = gui.update_display_color_logic("twitter.com")
        self.assertEqual(color, "#ff0000")


class MockScoreDisplayWithTransparency(MockScoreDisplay):
    """Extended mock for testing window transparency updates."""

    def __init__(self, score_tracker, config, update_interval=1000):
        super().__init__(score_tracker, config)
        self.update_interval = update_interval
        self._current_transparency = 1.0
        self._fade_active = False

    def _update_window_transparency(self):
        """Update window transparency based on flow mode state."""
        if not self.config.get_fade_window_on_flow_mode_enabled():
            # Mode is disabled, ensure window is fully opaque
            if self._current_transparency < 1.0:
                self._current_transparency = 1.0
                self.root.attributes("-alpha", self._current_transparency)
            self._fade_active = False
            return

        # Check if we're in flow state and should start fading
        flow_duration = self.score_tracker.get_flow_state_duration()
        flow_delay = self.config.get_flow_mode_delay_seconds()

        if self.score_tracker.is_in_flow_state() and flow_duration >= flow_delay:
            # We should be fading
            if not self._fade_active:
                # Just started fading
                self._fade_active = True

            # Calculate fade amount per update (update_interval is in ms, fade rate is per second)
            fade_per_update = (
                self.config.get_flow_mode_fade_rate_percent_per_second() / 100.0 * (self.update_interval / 1000.0)
            )

            # Apply fade (decrease transparency)
            new_transparency = max(0.0, self._current_transparency - fade_per_update)

            if new_transparency != self._current_transparency:
                self._current_transparency = new_transparency
                self.root.attributes("-alpha", self._current_transparency)
        else:
            # Not in flow state or haven't reached delay yet, reset transparency
            if self._current_transparency < 1.0 or self._fade_active:
                self._current_transparency = 1.0
                self.root.attributes("-alpha", self._current_transparency)
                self._fade_active = False


class TestGuiTransparencyUpdate(unittest.TestCase):
    """Test cases for GUI window transparency updates in flow mode."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_mock_gui(self, config_content):
        """Create a mock GUI with given configuration."""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))
        patterns = [
            {"regex": "github", "score": 10, "description": "GitHub"},
            {"regex": "twitter", "score": -5, "description": "Twitter"},
        ]
        score_tracker = ScoreTracker(patterns, default_score=0)
        gui = MockScoreDisplayWithTransparency(score_tracker, config)
        return gui

    def test_transparency_disabled_stays_opaque(self):
        """Test that transparency stays at 1.0 when fade mode is disabled."""
        config_content = """
fade_window_on_flow_mode_enabled = false
flow_mode_delay_seconds = 5
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        gui.score_tracker.update("github.com")
        self.assertTrue(gui.score_tracker.is_in_flow_state())

        # Update transparency
        gui._update_window_transparency()

        # Should remain fully opaque
        self.assertEqual(gui._current_transparency, 1.0)
        self.assertFalse(gui._fade_active)

    def test_transparency_fade_activates_after_delay(self):
        """Test that fade activates after flow state duration exceeds delay."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 5
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")
            self.assertTrue(gui.score_tracker.is_in_flow_state())

        # Before delay: should not fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 3)
            gui._update_window_transparency()
            self.assertEqual(gui._current_transparency, 1.0)
            self.assertFalse(gui._fade_active)

        # After delay: should start fading
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 6)
            gui._update_window_transparency()
            self.assertTrue(gui._fade_active)
            # With 10% fade rate and 1000ms interval, should fade 10% per update
            self.assertAlmostEqual(gui._current_transparency, 0.9, delta=0.01)

    def test_transparency_calculation_correct_fade_rate(self):
        """Test that transparency decreases at correct fade rate."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 20

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")

        # First update: 20% fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 1)
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.8, delta=0.01)

        # Second update: another 20% fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 2)
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.6, delta=0.01)

    def test_transparency_resets_on_exit_flow_state(self):
        """Test that transparency resets to 1.0 when exiting flow state."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -20
description = "Twitter"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state and fade
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.9, delta=0.01)

        # Exit flow state
        gui.score_tracker.update("twitter.com")
        self.assertFalse(gui.score_tracker.is_in_flow_state())

        # Transparency should reset
        gui._update_window_transparency()
        self.assertEqual(gui._current_transparency, 1.0)
        self.assertFalse(gui._fade_active)
        gui.root.attributes.assert_called_with("-alpha", 1.0)

    def test_transparency_minimum_zero(self):
        """Test that transparency doesn't go below 0.0."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 100

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")

        # Multiple updates with 100% fade rate should reach 0.0 and stay there
        for i in range(1, 5):
            with patch("src.score_tracker.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, i)
                gui._update_window_transparency()

        self.assertEqual(gui._current_transparency, 0.0)

    def test_transparency_update_interval_affects_fade(self):
        """Test that update interval affects fade calculation."""
        from datetime import datetime
        from unittest.mock import patch

        config_content = """
fade_window_on_flow_mode_enabled = true
flow_mode_delay_seconds = 0
flow_mode_fade_rate_percent_per_second = 10

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)
        gui.update_interval = 500  # 500ms instead of 1000ms

        # Enter flow state
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 0)
            gui.score_tracker.update("github.com")

        # With 500ms interval and 10% per second, should fade 5% per update
        with patch("src.score_tracker.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2024, 1, 1, 10, 0, 1)
            gui._update_window_transparency()
            self.assertAlmostEqual(gui._current_transparency, 0.95, delta=0.01)

    def test_transparency_no_change_when_already_at_target(self):
        """Test that transparency doesn't change when already at target state."""
        config_content = """
fade_window_on_flow_mode_enabled = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Already at 1.0, mode disabled
        gui._update_window_transparency()

        # Should not call attributes if no change
        gui.root.attributes.assert_not_called()


if __name__ == "__main__":
    unittest.main()
