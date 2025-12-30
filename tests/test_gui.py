#!/usr/bin/env python3
"""Tests for GUI module proximity detection."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# Try to import from src module
MAX_WINDOW_TITLE_LENGTH = None
get_status_text = None

try:
    from src.config import Config
    from src.score_tracker import ScoreTracker

    try:
        from src.gui import MAX_WINDOW_TITLE_LENGTH, get_status_text
    except (ImportError, ModuleNotFoundError):
        pass
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    from config import Config
    from score_tracker import ScoreTracker

    try:
        from gui import MAX_WINDOW_TITLE_LENGTH, get_status_text
    except (ImportError, ModuleNotFoundError):
        pass

# If tkinter is not available and import failed, define the constant and function here
# Note: This fallback is necessary for environments without tkinter (e.g., CI/headless systems)
# where src.gui cannot be imported. The logic is intentionally duplicated to maintain
# test functionality in these environments.
if MAX_WINDOW_TITLE_LENGTH is None:
    MAX_WINDOW_TITLE_LENGTH = 40

if get_status_text is None:

    def get_status_text(matched_pattern, window_title, default_score):
        """Fallback implementation of get_status_text for testing without tkinter."""
        if matched_pattern:
            description = matched_pattern.get("description", "")
            score_delta = matched_pattern.get("score", 0)
            score_sign = "+" if score_delta >= 0 else ""
            return f"{description} ({score_sign}{score_delta})"
        else:
            display_title = (
                window_title[:MAX_WINDOW_TITLE_LENGTH] + "..."
                if len(window_title) > MAX_WINDOW_TITLE_LENGTH
                else window_title
            )
            if default_score != 0:
                score_sign = "+" if default_score >= 0 else ""
                score_text = f"({score_sign}{default_score})"
                return f"No match: {display_title} {score_text}" if display_title else f"No match {score_text}"
            else:
                return display_title if display_title else "Watching..."


class MockScoreDisplay:
    """Mock ScoreDisplay class for testing proximity detection logic."""

    def __init__(self, score_tracker, config):
        self.score_tracker = score_tracker
        self.config = config
        self._mouse_in_proximity = False
        self._previous_always_on_top = None
        self._current_window_title = ""
        self._previous_window_title = ""
        self.root = MagicMock()

    def _apply_always_on_top(self):
        """Apply always_on_top setting to the window."""
        current_always_on_top = self.config.get_always_on_top()

        # Only update if the setting has changed
        if current_always_on_top != self._previous_always_on_top:
            self.root.attributes("-topmost", current_always_on_top)
            self._previous_always_on_top = current_always_on_top

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

    def _update_score_decreasing_topmost(self):
        """Update window topmost state based on score decreasing.

        This only applies when always_on_top_while_score_decreasing is enabled.
        This takes priority over other topmost settings.

        Returns:
            bool: True if this behavior took control of topmost, False otherwise
        """
        # Only apply if the feature is enabled
        if not self.config.get_always_on_top_while_score_decreasing():
            return False  # Feature not enabled, no priority taken

        # Check if score is currently decreasing
        is_decreasing = self.score_tracker.is_score_decreasing()

        if is_decreasing:
            # Score is decreasing: force topmost to True
            self.root.attributes("-topmost", True)
            return True  # Priority taken, topmost is now True
        else:
            # Score is not decreasing: restore configured topmost behavior
            # This ensures we don't leave the window stuck in a forced topmost state
            self._apply_always_on_top()
            return False  # No priority, let other behaviors take over

    def _on_ctrl_c(self, event):
        """Handle CTRL+C key press to copy previous window title to clipboard.

        This copies the previous window title (not the current one) because when the user
        presses CTRL+C, the focus is on this application, making it the active window.
        What we want is the window that was active before switching to this app.

        Args:
            event: tkinter event object
        """
        if self._previous_window_title:
            try:
                # Clear clipboard and set new content
                self.root.clipboard_clear()
                self.root.clipboard_append(self._previous_window_title)
                # Update() is needed to finalize the clipboard operation
                self.root.update()
            except Exception as e:
                # Silently ignore clipboard errors to not disrupt the main functionality
                print(f"Warning: Failed to copy to clipboard: {e}")


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


class TestGuiScoreDecreasingTopmost(unittest.TestCase):
    """Test cases for GUI score decreasing topmost feature."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def _create_mock_gui(self, config_content):
        """Helper to create a GUI with mocked tkinter components."""
        self.config_path.write_text(config_content)

        config = Config(str(self.config_path))
        patterns = config.get_window_patterns()
        score_tracker = ScoreTracker(
            patterns,
            config.get_default_score(),
            config.get_apply_default_score_mode(),
        )

        # Create GUI with MockScoreDisplay
        gui = MockScoreDisplay(score_tracker, config)

        return gui, gui.root

    def test_score_decreasing_topmost_feature_disabled(self):
        """Test that topmost is not updated when feature is disabled."""
        config_content = """
always_on_top_while_score_decreasing = false

[[window_patterns]]
regex = "test"
score = -5
description = "Test"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Simulate score decrease
        gui.score_tracker.update("test")

        # Call update
        result = gui._update_score_decreasing_topmost()

        # Should return False (no priority)
        self.assertFalse(result)

        # Should not call attributes
        mock_root.attributes.assert_not_called()

    def test_score_decreasing_topmost_score_decreasing(self):
        """Test that topmost is set to True when score is decreasing."""
        config_content = """
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        # Call update
        result = gui._update_score_decreasing_topmost()

        # Should return True (took priority)
        self.assertTrue(result)

        # Should set topmost to True
        mock_root.attributes.assert_called_once_with("-topmost", True)

    def test_score_decreasing_topmost_score_increasing(self):
        """Test that topmost is restored to configured value when score is not decreasing."""
        config_content = """
always_on_top = false
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # Increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)
        self.assertFalse(gui.score_tracker.is_score_decreasing())

        # Call update
        result = gui._update_score_decreasing_topmost()

        # Should return False (no priority)
        self.assertFalse(result)

        # Should restore topmost to False (always_on_top = false)
        mock_root.attributes.assert_called_once_with("-topmost", False)

    def test_score_decreasing_topmost_continuous_decrease(self):
        """Test that topmost stays True during continuous score decrease."""
        config_content = """
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First decrease
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), -5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

        # Reset mock
        mock_root.reset_mock()

        # Second decrease
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), -10)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

    def test_score_decreasing_topmost_stops_decreasing_restores_state(self):
        """Test that topmost is properly restored when score stops decreasing."""
        config_content = """
always_on_top = false
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score - should set topmost to True
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

        # Reset mock
        mock_root.reset_mock()

        # Now increase score again - should restore topmost to False (from always_on_top)
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 15)
        self.assertFalse(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertFalse(result)
        # Should restore topmost to False (always_on_top = false)
        mock_root.attributes.assert_called_with("-topmost", False)

    def test_score_decreasing_topmost_stops_with_always_on_top_true(self):
        """Test that topmost stays True when score stops decreasing and always_on_top is True."""
        config_content = """
always_on_top = true
always_on_top_while_score_decreasing = true

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        gui, mock_root = self._create_mock_gui(config_content)

        # First increase score
        gui.score_tracker.update("github")
        self.assertEqual(gui.score_tracker.get_score(), 10)

        # Then decrease score - should set topmost to True
        gui.score_tracker.update("twitter")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertTrue(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertTrue(result)
        mock_root.attributes.assert_called_with("-topmost", True)

        # Reset mock
        mock_root.reset_mock()

        # Now score stays same - should maintain topmost to True (from always_on_top)
        # Use apply_default_score_mode = false to avoid changing score
        config_content_no_default = """
always_on_top = true
always_on_top_while_score_decreasing = true
apply_default_score_mode = false

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"

[[window_patterns]]
regex = "twitter"
score = -5
description = "Twitter"
"""
        # Recreate GUI with updated config
        self.config_path.write_text(config_content_no_default)
        gui.config.load_config(exit_on_error=False)

        # Update score tracker with new config
        gui.score_tracker.update_config(
            gui.config.get_window_patterns(),
            gui.config.get_default_score(),
            gui.config.get_apply_default_score_mode(),
        )

        gui.score_tracker.update("unknown")
        self.assertEqual(gui.score_tracker.get_score(), 5)
        self.assertFalse(gui.score_tracker.is_score_decreasing())

        result = gui._update_score_decreasing_topmost()
        self.assertFalse(result)
        # Should keep topmost to True (always_on_top = true)
        mock_root.attributes.assert_called_with("-topmost", True)


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


class MockScoreDisplayWithStatusLabel(MockScoreDisplay):
    """Extended mock for testing status label updates."""

    def __init__(self, score_tracker, window_monitor, config):
        super().__init__(score_tracker, config)
        self.window_monitor = window_monitor
        self._previous_score = score_tracker.get_score()
        self.score_label = MagicMock()
        self.status_label = MagicMock()
        self._current_transparency = 1.0
        self._fade_active = False
        self.update_interval = 1000

    def update_display_status_logic(self, window_title):
        """Simulate the status label update logic from update_display."""
        # Update score
        score_changed, matched_pattern = self.score_tracker.update(window_title)

        # Update status label using the extracted function
        status_text = get_status_text(matched_pattern, window_title, self.score_tracker.default_score)
        self.status_label.config(text=status_text)


class TestGuiStatusLabelDisplay(unittest.TestCase):
    """Test cases for GUI status label display with window titles."""

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
        gui = MockScoreDisplayWithStatusLabel(score_tracker, window_monitor, config)
        return gui

    def test_status_label_shows_matched_pattern(self):
        """Test that status label shows description and score for matched pattern."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with matched pattern
        gui.update_display_status_logic("GitHub - Profile")

        # Verify status label shows matched pattern info
        gui.status_label.config.assert_called_with(text="GitHub (+10)")

    def test_status_label_shows_window_title_with_default_score_negative(self):
        """Test that status label shows window title with default score when no match and default_score < 0."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with no match
        gui.update_display_status_logic("Random Window Title")

        # Verify status label shows window title with default score
        gui.status_label.config.assert_called_with(text="No match: Random Window Title (-1)")

    def test_status_label_shows_window_title_with_default_score_positive(self):
        """Test that status label shows window title with default score when no match and default_score > 0."""
        config_content = """
default_score = 5

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with no match
        gui.update_display_status_logic("Some Application Window")

        # Verify status label shows window title with default score
        gui.status_label.config.assert_called_with(text="No match: Some Application Window (+5)")

    def test_status_label_shows_window_title_without_default_score_when_zero(self):
        """Test that status label shows only window title when no match and default_score = 0."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with no match
        gui.update_display_status_logic("Terminal - bash")

        # Verify status label shows only window title
        gui.status_label.config.assert_called_with(text="Terminal - bash")

    def test_status_label_truncates_long_window_title_with_default_score(self):
        """Test that long window titles are truncated when no match with default_score."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with long window title (over MAX_WINDOW_TITLE_LENGTH characters)
        long_title = "This is a very long window title that exceeds forty characters"
        gui.update_display_status_logic(long_title)

        # Verify status label shows truncated window title with ellipsis
        expected_text = f"No match: {long_title[:MAX_WINDOW_TITLE_LENGTH]}... (-1)"
        gui.status_label.config.assert_called_with(text=expected_text)

    def test_status_label_truncates_long_window_title_without_default_score(self):
        """Test that long window titles are truncated when no match without default_score."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with long window title (over MAX_WINDOW_TITLE_LENGTH characters)
        long_title = "This is a very long window title that exceeds forty characters"
        gui.update_display_status_logic(long_title)

        # Verify status label shows truncated window title with ellipsis
        expected_text = f"{long_title[:MAX_WINDOW_TITLE_LENGTH]}..."
        gui.status_label.config.assert_called_with(text=expected_text)

    def test_status_label_shows_watching_for_empty_window_title_without_default_score(self):
        """Test that status label shows 'Watching...' for empty window title without default_score."""
        config_content = """
default_score = 0

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with empty window title
        gui.update_display_status_logic("")

        # Verify status label shows "Watching..."
        gui.status_label.config.assert_called_with(text="Watching...")

    def test_status_label_shows_no_match_for_empty_window_title_with_default_score(self):
        """Test that status label shows 'No match (score)' for empty window title with default_score."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with empty window title
        gui.update_display_status_logic("")

        # Verify status label shows "No match (-1)"
        gui.status_label.config.assert_called_with(text="No match (-1)")

    def test_status_label_shows_window_title_with_special_characters(self):
        """Test that status label correctly shows window titles with special characters."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with special characters in window title
        special_title = "MyApp [Debug] - File.txt (Modified)"
        gui.update_display_status_logic(special_title)

        # Verify status label shows window title with special characters
        gui.status_label.config.assert_called_with(text=f"No match: {special_title} (-1)")

    def test_status_label_alternates_between_match_and_no_match(self):
        """Test that status label correctly alternates between matched and no-match states."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with matched pattern
        gui.update_display_status_logic("GitHub - Profile")
        gui.status_label.config.assert_called_with(text="GitHub (+10)")

        # Test with no match
        gui.update_display_status_logic("Random Window")
        gui.status_label.config.assert_called_with(text="No match: Random Window (-1)")

        # Test with matched pattern again
        gui.update_display_status_logic("GitHub - Issues")
        gui.status_label.config.assert_called_with(text="GitHub (+10)")

    def test_status_label_shows_window_title_exactly_max_length(self):
        """Test that window title with exactly MAX_WINDOW_TITLE_LENGTH characters is not truncated."""
        config_content = """
default_score = -1

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Test with exactly MAX_WINDOW_TITLE_LENGTH characters
        title_max_chars = "a" * MAX_WINDOW_TITLE_LENGTH
        gui.update_display_status_logic(title_max_chars)

        # Verify status label shows full window title without ellipsis
        gui.status_label.config.assert_called_with(text=f"No match: {title_max_chars} (-1)")


class TestClipboardCopyOnCtrlC(unittest.TestCase):
    """Test cases for clipboard copy on CTRL+C key press functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.toml"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_mock_gui(self, config_content):
        """Helper to create a mock GUI with given config."""
        self.config_path.write_text(config_content)
        config = Config(str(self.config_path))

        # Create patterns for testing
        patterns = [{"regex": "github", "score": 10, "description": "GitHub"}]
        score_tracker = ScoreTracker(patterns)

        # Create mock GUI with clipboard methods
        gui = MockScoreDisplay(score_tracker, config)
        gui.score_label = MagicMock()
        gui.status_label = MagicMock()

        # Mock clipboard methods
        gui.root.clipboard_clear = MagicMock()
        gui.root.clipboard_append = MagicMock()
        gui.root.update = MagicMock()

        return gui

    def test_ctrl_c_copies_current_window_title(self):
        """Test that CTRL+C copies the previous window title to clipboard."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set a previous window title (this is what should be copied)
        gui._previous_window_title = "Random Window Title"
        # Set a different current window title (this should NOT be copied)
        gui._current_window_title = "Cat Window Watcher - Cat is watching you -"

        # Simulate CTRL+C press
        gui._on_ctrl_c(None)

        # Verify clipboard methods were called with previous title
        gui.root.clipboard_clear.assert_called_once()
        gui.root.clipboard_append.assert_called_once_with("Random Window Title")
        gui.root.update.assert_called_once()

    def test_ctrl_c_with_empty_title_does_not_copy(self):
        """Test that CTRL+C does not copy when previous window title is empty."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set empty previous window title
        gui._previous_window_title = ""
        # Set non-empty current window title (should not be copied)
        gui._current_window_title = "Some Window"

        # Simulate CTRL+C press
        gui._on_ctrl_c(None)

        # Verify clipboard methods were not called
        gui.root.clipboard_clear.assert_not_called()
        gui.root.clipboard_append.assert_not_called()

    def test_ctrl_c_handles_errors_gracefully(self):
        """Test that clipboard errors are handled gracefully without crashing."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set a previous window title
        gui._previous_window_title = "Random Window Title"

        # Make clipboard_append raise an exception
        gui.root.clipboard_append.side_effect = Exception("Clipboard error")

        # Simulate CTRL+C press - should not raise exception
        try:
            gui._on_ctrl_c(None)
        except Exception as e:
            self.fail(f"_on_ctrl_c raised exception: {e}")

        # Verify clipboard_clear was called before the error
        gui.root.clipboard_clear.assert_called_once()

    def test_ctrl_c_can_copy_multiple_times(self):
        """Test that CTRL+C can copy the same previous title multiple times."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set a previous window title
        gui._previous_window_title = "Random Window Title"

        # First CTRL+C
        gui._on_ctrl_c(None)
        gui.root.clipboard_clear.assert_called_once()
        gui.root.clipboard_append.assert_called_once_with("Random Window Title")

        # Reset mocks
        gui.root.clipboard_clear.reset_mock()
        gui.root.clipboard_append.reset_mock()
        gui.root.update.reset_mock()

        # Second CTRL+C with same title - should copy again
        gui._on_ctrl_c(None)
        gui.root.clipboard_clear.assert_called_once()
        gui.root.clipboard_append.assert_called_once_with("Random Window Title")

    def test_ctrl_c_copies_different_titles(self):
        """Test that CTRL+C copies different previous window titles correctly."""
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set first previous window title
        gui._previous_window_title = "First Window"

        # First CTRL+C
        gui._on_ctrl_c(None)
        gui.root.clipboard_append.assert_called_once_with("First Window")

        # Reset mocks
        gui.root.clipboard_clear.reset_mock()
        gui.root.clipboard_append.reset_mock()
        gui.root.update.reset_mock()

        # Change previous window title
        gui._previous_window_title = "Second Window"

        # Second CTRL+C with different title
        gui._on_ctrl_c(None)
        gui.root.clipboard_append.assert_called_once_with("Second Window")

    def test_ctrl_c_copies_previous_not_current_title(self):
        """Test that CTRL+C copies the previous window title, not the current one.

        This verifies the fix for issue #37: When user presses CTRL+C, the focus
        shifts to the app itself, so we want the previous window title
        (before the app became active), not the current one.
        """
        config_content = """
[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
"""
        gui = self._create_mock_gui(config_content)

        # Set different current and previous window titles
        gui._current_window_title = "Cat Window Watcher - Cat is watching you -"
        gui._previous_window_title = "GitHub - Pull Requests"

        # Simulate CTRL+C press
        gui._on_ctrl_c(None)

        # Verify that the previous title is copied, not the current one
        gui.root.clipboard_append.assert_called_once_with("GitHub - Pull Requests")
        # Make sure it's NOT the current title
        self.assertNotEqual(gui.root.clipboard_append.call_args[0][0], "Cat Window Watcher - Cat is watching you -")


if __name__ == "__main__":
    unittest.main()
