# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that watches your active window and adjusts your score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Currently under development. There are bugs. Please refer to issues.

## ⚠️ Note on Temporary Implementation

This is a **temporary implementation for testing and validation purposes**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Clear logic: checks active window title every second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors your currently active window and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows your current score in a clean tkinter GUI.
- **Regex-based Window Matching**: Configure window title patterns using regular expressions.
- **Configurable Score Values**: Set custom score increments/decrements for each pattern.
- **Cross-Platform Compatibility**: Works on Linux, macOS, and Windows.
- **Lightweight**: Checks window titles once per second, minimal resource usage.
- **Screensaver Detection**: Score is not changed when the screensaver is active.

### About Screensaver Detection

This application detects if a screensaver is active and prevents score changes during its operation.

**Detection Method**: If the window title is an empty string, it is treated as a screensaver.

This practical and simple approach provides higher reliability compared to complex platform-specific implementations.
However, please note that special applications without a window title might also be treated as a screensaver.

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

The GUI features a dark theme with a large score display and a status indicating the current activity.

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
   - Windows: Works with built-in API (optionally `pywin32` for better support)

## Configuration

1. Copy the example configuration:
```bash
cp config.toml.example config.toml
```

2. Edit `config.toml` to customize window patterns and scores:

```toml
# Default score (applied when no pattern matches)
# Used to easily detect misconfigurations
# -1 (default) for easy detection, 0 to disable
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

#### Global Configuration Options

The following options are written at the top level of `config.toml` (outside of `[[window_patterns]]`):

- **verbose**: Whether to display configuration details at startup (default: false)
  - Set to `true` to display all configuration values when the application starts
  - Set to `false` (default) to not display configuration details
  - Enable for debugging or verifying settings
- **default_score**: Score applied when no pattern matches (default: -1)
  - Set to -1 (default) to make it easier to confirm if patterns are set correctly
  - Set to 0 if the score should not change when no match is found
  - If patterns are misconfigured, the score will continuously decrease, making it immediately noticeable
- **apply_default_score_mode**: Controls the application of the default score (default: true)
  - If `true`, `default_score` is applied when no pattern matches
  - If `false`, the score remains unchanged even if no pattern matches (score is maintained)
- **self_window_score**: Score applied when the app's own window is active (default: 0)
  - If you switch focus to the Cat Window Watcher window itself, this score will be applied instead of `default_score` or "no match"
  - Set to 0 (default) so the score does not change while checking the app
  - Set to a positive value to reward checking the score
  - Set to a negative value to discourage excessive score checking
- **mild_penalty_mode**: Mode to limit negative scores to -1 during a specified time window (default: false)
  - **Note**: This is a temporary implementation for testing purposes
  - Set to `true` to enable, `false` to disable
- **mild_penalty_start_hour**: Start hour for mild penalty mode (0-23, default: 22)
  - If `mild_penalty_mode` is enabled, negative scores are limited to -1 between `mild_penalty_start_hour` and `mild_penalty_end_hour`
- **mild_penalty_end_hour**: End hour for mild penalty mode (0-23, default: 23)
  - The time range includes both start and end hours
- **always_on_top**: Whether the window should always stay on top (default: true)
  - Set to `true` to keep the window always on top of other windows
  - Set to `false` for normal window behavior
- **hide_on_mouse_proximity**: Whether to move the window to the bottom when the mouse is near (default: true)
  - If `true`, the window automatically moves to the bottom when the mouse cursor approaches it, and returns to the top when the mouse moves away
  - If `false`, this feature is disabled
  - This feature only works if `always_on_top` is `true`
- **proximity_distance**: Distance for mouse proximity detection (in pixels, default: 50)
  - When the mouse cursor comes within this distance from the window, the window moves to the bottom
  - Increasing the value detects the mouse from further away
  - Decreasing the value requires the mouse to be closer to the window to react
- **always_on_top_while_score_decreasing**: Keep the window on top while the score is continuously decreasing (default: true)
  - If `true`, the window automatically moves to the top and stays there as long as the score is decreasing
  - If `false`, this feature is disabled
  - This helps you become aware when your concentration is dropping (e.g., browsing social media)
  - This setting takes precedence over other "always on top" settings while the score is decreasing
- **score_up_color**: Display color when the score increases or remains unchanged (default: "#ffffff" white)
  - Sets the font color when the score increases or does not change
  - Color codes are specified in hexadecimal format (e.g., "#ffffff")
- **score_down_color**: Display color when the score decreases (default: "#ff0000" red)
  - Sets the font color when the score decreases
  - Color codes are specified in hexadecimal format (e.g., "#ff0000")
- **reset_score_every_30_minutes**: Whether to reset the score to 0 every 30 minutes (default: true)
  - If `true`, the score is automatically reset to 0 at 00 and 30 minutes past the hour
  - If `false`, the score continues to accumulate
  - Similar to the Pomodoro Technique, this helps create the feeling of "focusing for just these 30 minutes"
  - Example: Even if the score is 100 at 10:29, it resets to 0 at 10:30, starting a new 30-minute period
- **fade_window_on_flow_mode_enabled**: Whether to gradually make the window transparent when in a flow state (default: false)
  - If `true`, after the score has been increasing for `flow_mode_delay_seconds`, the window gradually becomes transparent to aid concentration
  - If `false`, this feature is disabled
- **flow_mode_delay_seconds**: Wait time before starting fade (in seconds, default: 10)
  - After transitioning from a non-score-increasing state to a score-increasing state, waits for this many seconds before starting the fade effect
- **flow_mode_fade_rate_percent_per_second**: Flow mode transparency rate (transparency increase percentage per second, default: 1)
  - In flow mode, the window becomes more transparent by this percentage each second
  - Range: 1-100 (1 = slow fade, 100 = instant transparency)
- **default_transparency**: Initial transparency of the window (default: 1.0)
  - Sets the transparency/opacity of the window when it starts
  - Range: 0.0-1.0 (0.0 = completely transparent, 1.0 = completely opaque)
  - Useful if you want the window to be slightly transparent by default
  - Default: 1.0 - completely opaque
- **window_x / window_y**: Initial window position (X-coordinate / Y-coordinate, in pixels)
  - If both are specified, the window opens at that position
  - If either is not specified (or set to `null`), the system chooses a default position
  - Coordinates are in pixels relative to the top-left corner of the screen
  - Default: Not set (null) - system chooses position
- **copy_no_match_to_clipboard**: Automatically copy unmatched window titles to clipboard (default: false)
  - If `true`, any window title that doesn't match a pattern will be automatically copied to your clipboard
  - If `false`, this feature is disabled
  - Makes setting up new patterns easier - just switch to a window to get its title, then paste it into your config file
  - Each unique unmatched title is copied only once, preventing continuous clipboard updates

#### Window Pattern Specific Options

The following options are written within a `[[window_patterns]]` section:

- **regex**: Regular expression pattern to match against the window title (case-insensitive)
- **score**: Integer value to add to the score when the pattern matches (can be negative)
- **description**: Human-readable description displayed in the status area

## Usage

Run the application:
```bash
# Method 1: Run the script directly
python src/main.py

# Method 2: Run as a module
python -m src

# Method 3: Run with a custom config file
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

The GUI will display:
- The current score in large text
- A status showing the currently matched pattern or window title
- Automatically updates every second

## Examples

For more detailed configuration examples, please refer to the [examples/](examples/) directory.

### Example 1: Productivity Tracking

See [examples/example1_productivity.ja.toml](examples/example1_productivity.ja.toml)

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

See [examples/example2_study_time.ja.toml](examples/example2_study_time.ja.toml)

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

### Example 3: Always on Top Mode with Auto-Hide on Mouse Proximity

See [examples/example3_always_on_top.ja.toml](examples/example3_always_on_top.ja.toml)

```toml
# Keep the window always on top, but automatically move it to the bottom when the mouse is near
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
description = "GitHub"
regex = "github"
score = 10
```

With this configuration, the window will generally stay on top, but when the mouse cursor approaches within 50 pixels, it will automatically move to the bottom, returning to the top when the mouse moves away. This is designed to not interfere with your work.

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

- **config.py**: Reads and manages TOML configuration.
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
Uses built-in AppleScript. No additional dependencies required.

### Windows
Works with built-in Windows API. For better compatibility, install:
```bash
pip install pywin32
```

## License

See the LICENSE file for details.

*Big Brother is watching you. But this time, it's a cat. 🐱*