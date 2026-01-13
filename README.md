# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that watches your active window and adjusts your score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Under development. There are bugs. Please refer to issues.

## ⚠️ Note on Provisional Implementation

This is a **provisional implementation for testing and validation**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Easy-to-understand logic: checks active window title every second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and clarity.

## Concept

The application monitors your currently active window and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows your current score in a clean tkinter GUI
- **Regex-Based Window Matching**: Configure window title patterns using regular expressions
- **Configurable Score Values**: Set custom score increments/decrements for each pattern
- **Cross-Platform Compatible**: Works on Linux, macOS, and Windows
- **Lightweight**: Checks window title once per second, minimal resource usage

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

The GUI features a dark theme, a large score display, and status indicating the current activity.

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

3. Install dependencies (if needed):
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
# Default score (applied when no pattern matches)
# Used to easily detect misconfigurations.
# Set to -1 (default) for easy detection, 0 to disable.
default_score = -1

[[window_patterns]]
description = "GitHub"
regex = "github"
score = 10

[[window_patterns]]
description = "Twitter/X"
regex = "twitter|x\\.com"
score = -5
```

### Configuration Options

- **verbose**: Whether to display configuration details on startup (default: false)
  - If set to `true`, all configuration values will be displayed when the application starts
  - If set to `false`, configuration details will not be displayed (default)
  - Enable this when debugging or verifying your settings
- **default_score**: Score applied when no pattern matches (default: -1)
  - Setting to -1 (default) makes it easier to verify that patterns are configured correctly
  - Setting to 0 means the score does not change if no pattern matches
  - If patterns are misconfigured, the score will continuously decrease, making it immediately noticeable
- **apply_default_score_mode**: Controls application of default score (default: true)
  - If set to `true`, `default_score` is applied when no pattern matches
  - If set to `false`, the score does not change even if no pattern matches (score is maintained)
- **self_window_score**: Score applied when the app's own window is active (default: 0)
  - If you switch focus to the Cat Window Watcher window itself, this score is applied instead of `default_score` or "no match"
  - Setting to 0 (default) means the score does not change while you are checking the app
  - Setting to a positive value rewards checking the score
  - Setting to a negative value discourages excessive score checking
- **mild_penalty_mode**: Mode to restrict negative scores to -1 during specified hours (default: false)
  - **Note**: This is a provisional implementation for testing purposes
  - Set to `true` to enable, `false` to disable
- **mild_penalty_start_hour**: Start hour for mild penalty mode (0-23, default: 22)
  - If `mild_penalty_mode` is enabled, negative scores are restricted to -1 during the period from `mild_penalty_start_hour` to `mild_penalty_end_hour`
- **mild_penalty_end_hour**: End hour for mild penalty mode (0-23, default: 23)
  - The time range includes both the start and end hours
- **always_on_top**: Whether to always display the window on top (default: true)
  - If set to `true`, the window will always be displayed above other windows
  - If set to `false`, it will behave as a normal window
- **hide_on_mouse_proximity**: Whether to move the window to the background when the mouse approaches (default: true)
  - If set to `true`, the window automatically moves to the background when the mouse cursor approaches it, and returns to the foreground when it moves away
  - If set to `false`, this feature is disabled
  - This feature only works if `always_on_top` is `true`
- **proximity_distance**: Mouse proximity detection distance (in pixels, default: 50)
  - When the mouse cursor comes within this distance of the window, the window moves to the background
  - A larger value detects the mouse from further away
  - A smaller value requires the mouse to be closer to the window to react
- **always_on_top_while_score_decreasing**: Keep window on top while score is decreasing (default: true)
  - If set to `true`, the window will automatically display on top while the score is decreasing
  - If set to `false`, this feature is disabled
  - This helps you notice when your focus is dropping (e.g., when looking at social media)
  - This takes precedence over other always-on-top settings while the score is decreasing
- **score_up_color**: Display color when score increases or stays the same (default: "#ffffff" white)
  - Sets the font color when the score increases or remains unchanged
  - Color codes are specified in hexadecimal format (e.g., "#ffffff")
- **score_down_color**: Display color when score decreases (default: "#ff0000" red)
  - Sets the font color when the score decreases
  - Color codes are specified in hexadecimal format (e.g., "#ff0000")
- **reset_score_every_30_minutes**: Whether to reset score to 0 every 30 minutes (default: true)
  - If set to `true`, the score will automatically reset to 0 at XX:00 and XX:30 every hour
  - If set to `false`, the score will continue to accumulate
  - Similar to the Pomodoro Technique, this helps create the feeling of "focusing for just these 30 minutes"
  - Example: Even if the score is 100 at 10:29, it will reset to 0 at 10:30, starting a new 30-minute period
- **fade_window_on_flow_mode_enabled**: Whether to gradually fade the window when in a flow state (default: false)
  - If set to `true`, after the score-increasing state continues for `flow_mode_delay_seconds`, the window will gradually become transparent to help you focus
  - If set to `false`, this feature is disabled
- **flow_mode_delay_seconds**: Delay before fade starts (in seconds, default: 10)
  - After transitioning from a non-score-increasing state to a score-increasing state, waits for this many seconds before starting the fade effect
- **flow_mode_fade_rate_percent_per_second**: Flow mode transparency rate (percentage increase in transparency per second, default: 1)
  - During flow mode, the window will become more transparent by this percentage each second
  - Range: 1-100 (1 = slow fade, 100 = instant transparency)
- **default_transparency**: Initial window transparency (default: 1.0)
  - Sets the transparency/opacity of the window when it starts
  - Range: 0.0-1.0 (0.0 = completely transparent, 1.0 = completely opaque)
  - Useful if you want the window to be slightly transparent by default
  - Default: 1.0 - fully opaque
- **window_x / window_y**: Initial window position (X / Y coordinates, in pixels)
  - If both are specified, the window will open at that position
  - If either is not specified (or set to null), the system will choose a default position
  - Coordinates are in pixels relative to the top-left corner of the screen
  - Default: Unset (null) - System chooses position
- **copy_no_match_to_clipboard**: Automatically copy unmatched window titles to clipboard (default: false)
  - If set to `true`, any window title that doesn't match a pattern will be automatically copied to the clipboard
  - If set to `false`, this feature is disabled
  - Makes it easier to set up new patterns – just switch to a window to get its title and paste it into the config file
  - Each unique unmatched title is copied only once, so the clipboard won't be repeatedly updated
- **regex**: Regular expression pattern to match window titles (case-insensitive)
- **score**: Integer value to add to the score when the pattern matches (can be negative)
- **description**: Human-readable description to display in the status area

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
- Your current score in large text
- Status showing the currently matched pattern or window title
- Automatically updates every second

## Examples

### Example 1: Productivity Tracking
```toml
[[window_patterns]]
description = "Coding"
regex = "github|gitlab"
score = 10

[[window_patterns]]
description = "Social Media"
regex = "twitter|facebook|instagram"
score = -5
```

### Example 2: Study Time
```toml
[[window_patterns]]
description = "Reading"
regex = "pdf|documentation|docs"
score = 8

[[window_patterns]]
description = "Entertainment"
regex = "youtube|netflix"
score = -10
```

### Example 3: Always-On-Top Mode with Auto-Background on Mouse Proximity
```toml
# Always display the window on top, and automatically move it to the background when the mouse approaches
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
description = "GitHub"
regex = "github"
score = 10
```

With this setting, the window will normally be displayed on top, but when the mouse cursor comes within 50 pixels, it will automatically move to the background. When the mouse moves away, it will return to the foreground. This is designed to not interfere with your work.

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

- **config.py**: Handles loading and managing TOML configurations
- **window_monitor.py**: Cross-platform window title detection
- **score_tracker.py**: Matches window titles to patterns and tracks the score
- **gui.py**: tkinter-based score display interface
- **main.py**: Application entry point and orchestration

## Platform-Specific Notes

### Linux
Requires `xdotool` or `xprop`:
```bash
sudo apt-get install xdotool  # Debian/Ubuntu
```

### macOS
Uses built-in AppleScript. No additional dependencies required.

### Windows
Works with built-in Windows APIs. Install for better compatibility:
```bash
pip install pywin32
```

## License

See the LICENSE file for details.

*Big Brother is watching you. But this time, it's a cat. 🐱*