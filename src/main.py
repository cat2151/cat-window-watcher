#!/usr/bin/env python3
"""Main entry point for cat-window-watcher."""

import argparse
import sys
from pathlib import Path

try:
    from .config import Config
    from .gui import ScoreDisplay
    from .score_tracker import ScoreTracker
    from .window_monitor import WindowMonitor
except ImportError:
    from config import Config
    from gui import ScoreDisplay
    from score_tracker import ScoreTracker
    from window_monitor import WindowMonitor


def main():
    """Main function to run cat-window-watcher."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Cat Window Watcher - Cat is watching you -",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.toml",
        help="Path to configuration file (default: config.toml)",
    )
    args = parser.parse_args()

    # Check if config file exists
    if not Path(args.config).exists():
        print(f"Error: Configuration file '{args.config}' not found.")
        print("\nPlease create a config.toml file with window patterns.")
        print("See README.md for configuration examples.")
        sys.exit(1)

    try:
        # Load configuration
        config = Config(args.config)

        # Create window monitor
        window_monitor = WindowMonitor()

        # Create score tracker
        score_tracker = ScoreTracker(config.get_window_patterns(), config.get_default_score())

        # Create and run GUI
        gui = ScoreDisplay(score_tracker, window_monitor, config)
        gui.run()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
