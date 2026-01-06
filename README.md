# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that monitors active windows and adjusts a score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Under development. Bugs may exist. Please refer to the issues.

## ⚠️ Important Note on Provisional Implementation

This is a **provisional implementation for testing and validation**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Clear logic: checks active window title every second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors currently active windows and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows current score in a clean tkinter GUI
- **Regex-Based Window Matching**: Configure window title patterns using regular expressions
- **Configurable Score Values**: Set custom score increments/decrements for each pattern
- **Cross-Platform Compatibility**: Works on Linux, macOS, and Windows
- **Lightweight**: Checks window titles once per second, minimal resource usage

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
# Default score (applied when no pattern matches)
# Used to easily detect misconfigurations
# Set to -1 (default) to easily detect misconfigurations, 0 to disable
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

- **verbose**: Whether to display configuration details on startup (default: false)
  - If set to `true`, all configuration values will be displayed when the application starts.
  - If set to `false`, configuration details will not be displayed (default).
  - Enable this for debugging or when you need to verify settings.
- **default_score**: Default score (applied when no pattern matches) (default: -1)
  - Setting to -1 (default) makes it easier to verify if patterns are correctly configured.
  - Setting to 0 means the score will not change if no pattern matches.
  - If patterns are incorrectly configured, you'll quickly notice as the score will continuously decrease.
- **apply_default_score_mode**: Control application of default score (default: true)
  - If set to `true`, `default_score` will be applied when no pattern matches.
  - If set to `false`, the score will not change even if no pattern matches (score is maintained).
- **self_window_score**: Score applied when the app's own window is active (default: 0)
  - If you switch focus to the Cat Window Watcher window itself, this score will be applied instead of `default_score` or 'no match'.
  - Setting to 0 (default) means the score will not change while you are checking the app.
  - Setting to a positive value rewards checking your score.
  - Setting to a negative value discourages excessive score checking.
- **mild_penalty_mode**: Mode to limit negative scores to -1 during specified hours (default: false)
  - **Note**: This is a provisional implementation for testing purposes.
  - Set to `true` to enable, `false` to disable.
- **mild_penalty_start_hour**: Start hour for mild penalty mode (0-23, default: 22)
  - If `mild_penalty_mode` is enabled, negative scores will be limited to -1 during the time range from `mild_penalty_start_hour` to `mild_penalty_end_hour`.
- **mild_penalty_end_hour**: End hour for mild penalty mode (0-23, default: 23)
  - The time range includes both the start and end hours.
- **always_on_top**: Whether to keep the window always on top (default: true)
  - If set to `true`, the window will always appear above other windows.
  - If set to `false`, it will behave as a normal window.
- **hide_on_mouse_proximity**: Whether to move the window to the background when the mouse approaches (default: true)
  - If set to `true`, when the mouse cursor approaches the window, it will automatically move to the background, and return to the foreground when the mouse moves away.
  - If set to `false`, this feature is disabled.
  - This feature only works if `always_on_top` is `true`.
- **proximity_distance**: Mouse proximity detection distance (in pixels, default: 50)
  - When the mouse cursor enters within this distance from the window, the window will move to the background.
  - Increasing the value will detect the mouse from further away.
  - Decreasing the value means it will only react when the mouse is closer to the window.
- **always_on_top_while_score_decreasing**: Keep window always on top while score is decreasing (default: true)
  - If set to `true`, the window will automatically be brought to the foreground while the score is decreasing.
  - If set to `false`, this feature is disabled.
  - This helps you notice when your focus is dropping (e.g., when browsing social media).
  - This takes precedence over other 'always on top' settings while the score is decreasing.
- **score_up_color**: Display color when score increases or doesn't change (default: "#ffffff" white)
  - Sets the font color when the score increases or remains unchanged.
  - Color codes are specified in hexadecimal format (e.g., "#ffffff").
- **score_down_color**: Display color when score decreases (default: "#ff0000" red)
  - Sets the font color when the score decreases.
  - Color codes are specified in hexadecimal format (e.g., "#ff0000").
- **reset_score_every_30_minutes**: Whether to reset the score to 0 every 30 minutes (default: true)
  - If set to `true`, the score will automatically reset to 0 at 00 and 30 minutes past the hour.
  - If set to `false`, the score will continue to accumulate.
  - Similar to the Pomodoro Technique, this helps create the idea of 'focusing for just the current 30 minutes'.
  - Example: Even if your score is 100 at 10:29, it will reset to 0 at 10:30, and a new 30-minute period begins.
- **fade_window_on_flow_mode_enabled**: Whether to gradually fade the window to transparent when in a flow state (default: false)
  - If set to `true`, after the score has been increasing for `flow_mode_delay_seconds`, the window will gradually become transparent to aid concentration.
  - If set to `false`, this feature is disabled.
- **flow_mode_delay_seconds**: Wait time before fade starts (in seconds, default: 10)
  - After transitioning from a non-score-increasing state to a score-increasing state, it waits this number of seconds before starting the fade effect.
- **flow_mode_fade_rate_percent_per_second**: Flow mode transparency rate (transparency increase per second, in percent, default: 1)
  - During flow mode, the window becomes this percentage more transparent each second.
  - Range: 1-100 (1 = slow fade, 100 = instant transparency).
- **default_transparency**: Initial window transparency (default: 1.0)
  - Sets the transparency/opacity of the window on startup.
  - Range: 0.0-1.0 (0.0 = fully transparent, 1.0 = fully opaque).
  - Useful if you want the window to be slightly transparent by default.
  - Default: 1.0 - fully opaque.
- **window_x / window_y**: Initial window position (X coordinate / Y coordinate, in pixels)
  - If both are specified, the window will open at that position.
  - If either is not specified (or set to null), the system will choose the default position.
  - Coordinates are in pixels, relative to the top-left corner of the screen.
  - Default: Unset (null) - system chooses position.
- **copy_no_match_to_clipboard**: Automatically copy unmatched window titles to clipboard (default: false)
  - If set to `true`, window titles that do not match any pattern will automatically be copied to the clipboard.
  - If set to `false`, this feature is disabled.
  - Makes it easy to configure new patterns - simply switch to a window to get its title, then paste it into the configuration file.
  - Each unique unmatched title is copied only once, so the clipboard won't be updated repeatedly.
- **regex**: Regular expression pattern to match window title (case-insensitive)
- **score**: Integer value to add to the score when a pattern matches (can be negative)
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
- The current score in large text
- Status showing the currently matched pattern or window title
- Automatically updates every second

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

### Example 3: Always On Top Mode with Auto-Background on Mouse Proximity
```toml
# Keep the window always on top, but automatically move it to the background when the mouse approaches
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
```

With this configuration, the window will typically remain always on top. However, if the mouse cursor approaches within 50 pixels, it will automatically move to the background, and return to the foreground when the mouse moves away. This is designed to not interfere with your work.

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
Verify code quality:
```bash
ruff format --check src/ tests/
ruff check src/ tests/
```

## Architecture

The application is composed of several modules:

- **config.py**: Loads and manages TOML configurations
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
Works with built-in Windows API. Install for better compatibility:
```bash
pip install pywin32
```

## License

See the LICENSE file for details.

*Big Brother is watching you. But this time, it's a cat. 🐱*