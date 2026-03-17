#!/usr/bin/env python3
"""Tests for GUI module - proximity detection."""

import tempfile
import unittest
from pathlib import Path

try:
    from tests.gui_mock_base import Config, MockScoreDisplay, ScoreTracker
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from gui_mock_base import Config, MockScoreDisplay, ScoreTracker


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


if __name__ == "__main__":
    unittest.main()
