# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that tracks your active window and adjusts a score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Under development. Contains bugs. Please refer to issues.

## ⚠️ Note on Provisional Implementation

This is a **provisional implementation for testing and validation**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Clear logic: checking the active window title every second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors your currently active window and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows the current score in a clean tkinter GUI.
- **Regex-based Window Matching**: Configure window title patterns using regular expressions.
- **Configurable Score Values**: Set custom score increments/decrements for each pattern.
- **Cross-Platform Compatibility**: Works on Linux, macOS, and Windows.
- **Lightweight**: Checks window titles once per second, minimal resource usage.

## Appearance

```
╔════════════════════════════════════════════════════════════╗
║   Cat Window Watcher - Cat is watching you -               ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║                                                            ║
║                       Score: 42                            ║
║                                                            ║
║                                                            ║
║                      GitHub (+10)                          ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

The GUI features a dark theme, a large score display, and a status showing the current activity.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cat2151/cat-window-watcher.git
cd cat-window-watcher
```

2. Ensure Python 3.12 or higher is installed:
```bash
python --version
```

3. Install dependencies (if necessary):
   - Linux: `xdotool` or `xprop` (usually pre-installed)
   - macOS: Built-in AppleScript support
   - Windows: Works with built-in APIs (optionally use `pywin32` for better support)

## Configuration

1. Copy the example configuration:
```bash
cp config.toml.example config.toml
```

2. Edit `config.toml` to customize window patterns and scores:

```toml
# Default score (applied if no pattern matches)
# Used to easily detect misconfigurations
# -1 (default) for easy detection of misconfigurations, 0 to disable
default_score = -1

[[window_patterns]]
regex = "github"           # Regex pattern to match window title
score = 10                 # Score change when this window is active
description = "GitHub"     # Display description

[[window_patterns]]
regex = "twitter|x\\.com"
score = -5
description = "Twitter/X"
```

### Configuration Options

- **default_score**: Score applied when no pattern matches (default: -1)
  - Setting it to -1 (default) makes it easier to detect if patterns are configured correctly.
  - Setting it to 0 means the score won't change if no pattern matches.
  - If patterns are configured incorrectly, the score will continuously decrease, making it immediately noticeable.
- **apply_default_score_mode**: Controls the application of `default_score` (default: true)
  - If set to `true`, `default_score` is applied when no pattern matches.
  - If set to `false`, the score remains unchanged even if no pattern matches (score is maintained).
- **self_window_score**: Score applied when the application's own window is active (default: 0)
  - When you switch focus to the Cat Window Watcher window itself, this score is applied instead of `default_score` or "no match".
  - If set to 0 (default), the score won't change while you're checking the app.
  - If set to a positive value, it rewards checking the score.
  - If set to a negative value, it discourages excessive score checking.
- **mild_penalty_mode**: Mode to limit negative scores to -1 during specified hours (default: false)
  - **Note**: This is a provisional implementation for testing purposes.
  - Set to `true` to enable, `false` to disable.
- **mild_penalty_start_hour**: Start hour for mild penalty mode (0-23, default: 22)
  - If `mild_penalty_mode` is enabled, negative scores are limited to -1 during the time range from `mild_penalty_start_hour` to `mild_penalty_end_hour`.
- **mild_penalty_end_hour**: End hour for mild penalty mode (0-23, default: 23)
  - The time range includes both the start and end hours.
- **always_on_top**: Whether to keep the window always on top (default: true)
  - If set to `true`, the window will always appear above other windows.
  - If set to `false`, it behaves as a normal window.
- **hide_on_mouse_proximity**: Whether to move the window to the back when the mouse is nearby (default: true)
  - If set to `true`, when the mouse cursor approaches the window, it automatically moves to the back, and returns to the front when the mouse moves away.
  - If set to `false`, this feature is disabled.
  - This feature only works if `always_on_top` is `true`.
- **proximity_distance**: Distance for mouse proximity detection (in pixels, default: 50)
  - When the mouse cursor comes within this distance of the window, the window moves to the back.
  - Increasing the value detects the mouse from farther away.
  - Decreasing the value requires the mouse to be closer to the window to react.
- **always_on_top_while_score_decreasing**: Keep window always on top while score is decreasing (default: true)
  - If set to `true`, the window will automatically display itself always on top when the score is decreasing.
  - If set to `false`, this feature is disabled.
  - This helps you notice when your focus is dropping (e.g., when browsing social media).
  - Takes precedence over other "always on top" settings while the score is decreasing.
- **score_up_color**: Display color when the score increases or doesn't change (default: "#ffffff" white)
  - Sets the font color when the score increases or remains unchanged.
  - Color codes should be specified in hexadecimal format (e.g., "#ffffff").
- **score_down_color**: Display color when the score decreases (default: "#ff0000" red)
  - Sets the font color when the score decreases.
  - Color codes should be specified in hexadecimal format (e.g., "#ff0000").
- **reset_score_every_30_minutes**: Whether to reset the score to 0 every 30 minutes (default: true)
  - If set to `true`, the score automatically resets to 0 at 00 and 30 minutes past the hour.
  - If set to `false`, the score continues to accumulate.
  - Similar to the Pomodoro Technique, it helps create the feeling of "focusing for just these 30 minutes".
  - Example: Even if the score is 100 at 10:29, it resets to 0 at 10:30, starting a new 30-minute period.
- **fade_window_on_flow_mode_enabled**: Whether to gradually make the window transparent in flow state (default: false)
  - If set to `true`, after `flow_mode_delay_seconds` of score increasing, the window will gradually become transparent to aid concentration.
  - If set to `false`, this feature is disabled.
- **flow_mode_delay_seconds**: Wait time before fading starts (in seconds, default: 10)
  - After transitioning from a non-score-increasing state to a score-increasing state, it waits for this many seconds before starting the fade effect.
- **flow_mode_fade_rate_percent_per_second**: Flow mode transparency speed (transparency increase rate per second, in percent, default: 1)
  - During flow mode, the window becomes transparent by this percentage every second.
  - Range: 1-100 (1 = slow fade, 100 = instant transparency).
- **default_transparency**: Initial window transparency (default: 1.0)
  - Sets the transparency/opacity of the window when it starts.
  - Range: 0.0-1.0 (0.0 = fully transparent, 1.0 = fully opaque).
  - Useful if you want the window to be slightly transparent by default.
  - Default: 1.0 - fully opaque.
- **window_x / window_y**: Initial window position (X / Y coordinates, in pixels)
  - If both are specified, the window will open at that position.
  - If either is not specified (or set to `null`), the system chooses the default position.
  - Coordinates are in pixels relative to the top-left corner of the screen.
  - Default: Not set (`null`) - system chooses position.
- **copy_no_match_to_clipboard**: Automatically copy unmatched window titles to clipboard (default: false)
  - If set to `true`, any window title that doesn't match a pattern will be automatically copied to the clipboard.
  - If set to `false`, this feature is disabled.
  - Makes configuring new patterns easy - just switch to the window to get its title, then paste into the config file.
  - Each unique unmatched title is copied only once, so the clipboard won't be repeatedly updated.
- **regex**: Regular expression pattern to match window titles (case-insensitive).
- **score**: Integer value to add to the score when the pattern matches (can be negative).
- **description**: Human-readable description displayed in the status area.

## Usage

Run the application:
```bash
# Method 1: Run the script directly
python src/main.py

# Method 2: Run as a module
python -m src

# Method 3: Run with a custom configuration file
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

The GUI will display:
- The current score in large text
- A status showing the currently matched pattern or window title
- Automatic updates every second

## Examples

### Example 1: Productivity Tracking
```toml
[[window_patterns]]
regex = "github|gitlab"
score = 10
description = "Coding"

[[window_patterns]]
regex = "twitter|facebook|instagram"
score = -5
description = "Social Media"
```

### Example 2: Study Time
```toml
[[window_patterns]]
regex = "pdf|documentation|docs"
score = 8
description = "Reading"

[[window_patterns]]
regex = "youtube|netflix"
score = -10
description = "Entertainment"
```

### Example 3: Always-on-top mode with automatic move-to-back on mouse proximity
```toml
# Always keep the window on top, but automatically move it to the back when the mouse approaches
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
```

With this configuration, the window will normally be displayed always on top, but when the mouse cursor approaches within 50 pixels, it will automatically move to the back, and return to the front when the mouse moves away. This is designed to not interfere with your work.

## Development

### Running Tests
```bash
python -m unittest discover tests/ -v
```

### Code Formatting
Format code before committing:
```bash
ruff format src/ tests/
ruff check --fix src/ tests/
```

### Linting
Validate code quality:
```bash
ruff format --check src/ tests/
ruff check src/ tests/
```

## Architecture

The application is composed of several modules:

- **config.py**: Reads and manages TOML configurations.
- **window_monitor.py**: Cross-platform window title detection.
- **score_tracker.py**: Matches window titles to patterns and tracks the score.
- **gui.py**: tkinter-based score display interface.
- **main.py**: Application entry point and orchestration.

## Platform-Specific Notes

### Linux
Requires `xdotool` or `xprop`:
```bash
sudo apt-get install xdotool  # Debian/Ubuntu
```

### macOS
Uses built-in AppleScript. No additional dependencies are required.

### Windows
Works with built-in Windows API. For better compatibility, install:
```bash
pip install pywin32
```

## License

See the LICENSE file for details.

*Big Brother is watching you. But this time, it's a cat. 🐱*