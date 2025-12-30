# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that watches active windows and adjusts your score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Under development. There are bugs. Please refer to issues.

## ⚠️ Important Note on Provisional Implementation

This is a **provisional implementation for testing and validation**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Clear logic: checks active window titles every second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors currently active windows and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows current score in a clean tkinter GUI
- **Regex-based Window Matching**: Configure window title patterns using regular expressions
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

The GUI features a dark theme, a large score display, and a status area showing current activity.

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
# Used to easily detect misconfigurations
# -1 (default) makes it easy to detect misconfigurations, set to 0 to disable
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
  - Setting to -1 (default) makes it easy to verify if patterns are correctly configured.
  - Setting to 0 means the score will not change if no match is found.
  - If patterns are misconfigured, you'll quickly notice as the score will continuously decrease.
- **always_on_top**: Whether the window should always stay on top (default: false)
  - If set to `true`, the window will always be displayed above other windows.
  - If set to `false`, it behaves as a normal window.
- **hide_on_mouse_proximity**: Whether to move the window to the background when the mouse approaches (default: false)
  - If set to `true`, the window will automatically move to the background when the mouse cursor approaches it, and return to the foreground when it moves away.
  - If set to `false`, this feature is disabled.
  - This feature only works if `always_on_top` is `true`.
- **proximity_distance**: Distance for mouse proximity detection (in pixels, default: 50)
  - The window will move to the background when the mouse cursor enters within this distance from the window.
  - Increasing the value detects the mouse from a greater distance.
  - Decreasing the value requires the mouse to be closer to the window to react.
- **always_on_top_while_score_decreasing**: Keep window on top while score is continuously decreasing (default: false)
  - If set to `true`, the window will automatically be brought to the foreground while the score is decreasing.
  - If set to `false`, this feature is disabled.
  - This helps you notice when your focus is dropping (e.g., when browsing social media).
  - This takes precedence over other always-on-top settings while the score is decreasing.
- **reset_score_every_30_minutes**: Whether to reset the score to 0 every 30 minutes (default: false)
  - If set to `true`, the score will automatically reset to 0 at XX:00 and XX:30 every hour.
  - If set to `false`, the score will continue to accumulate.
  - Similar to the Pomodoro Technique, this helps create a mindset of 'just focusing for these 30 minutes'.
  - Example: If your score is 100 at 10:29, it will reset to 0 at 10:30, starting a new 30-minute period.
- **copy_no_match_to_clipboard**: Automatically copy unmatched window titles to clipboard (default: false)
  - If set to `true`, any window title that does not match any pattern will automatically be copied to the clipboard.
  - If set to `false`, this feature is disabled.
  - This simplifies setting up new patterns – just switch to a window to get its title, then paste it into your configuration file.
  - Each unique unmatched title is copied only once, preventing repeated clipboard updates.
- **regex**: Regular expression pattern to match window titles (case-insensitive)
- **score**: Integer value to add to the score when the pattern matches (can be negative)
- **description**: Human-readable description displayed in the status area

## Usage

Run the application:
```bash
# Method 1: Run script directly
python src/main.py

# Method 2: Run as module
python -m src

# Method 3: Run with custom config file
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

The GUI will display:
- The current score in large text
- Status showing the currently matched pattern or window title
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

### Example 3: Always-on-Top Mode with Automatic Backgrounding on Mouse Proximity
```toml
# Always display window on top, but automatically move to background when mouse approaches
always_on_top = true
hide_on_mouse_proximity = true
proximity_distance = 50

[[window_patterns]]
regex = "github"
score = 10
description = "GitHub"
```

With this configuration, the window will normally stay on top, but will automatically move to the background when the mouse cursor approaches within 50 pixels, and return to the foreground when the mouse moves away. This is designed to minimize disruption to your work.

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

The application consists of several modules:

- **config.py**: Reads and manages TOML configuration
- **window_monitor.py**: Cross-platform window title detection
- **score_tracker.py**: Matches window titles to patterns and tracks the score
- **gui.py**: tkinter-based score display interface
- **main.py**: Application entry point and orchestration

## Platform-Specific Notes

### Linux
`xdotool` or `xprop` is required:
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