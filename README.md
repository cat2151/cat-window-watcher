# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that watches your active windows and adjusts a score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Under development. There are known bugs. Please refer to issues.

## ⚠️ Note on Provisional Implementation

This is a **provisional implementation for testing and validation**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Straightforward logic: checks the active window title every second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors your currently active window and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows your current score in a clean tkinter GUI
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

The GUI features a dark theme, a large score display, and a status area showing the current activity.

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
   - Windows: Works with built-in API (optionally use `pywin32` for better support)

## Configuration

1. Copy the example configuration:
```bash
cp config.toml.example config.toml
```

2. Edit `config.toml` to customize window patterns and scores:

```toml
# Default score (applied if no pattern matches)
# Used to easily detect configuration errors
# Set to -1 (default) to easily detect config errors, set to 0 to disable
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

- **default_score**: The score applied when no pattern matches (default: -1)
  - Setting to -1 (default) makes it easier to verify if patterns are configured correctly
  - Setting to 0 means the score won't change if no match occurs
  - If patterns are incorrectly configured, the score will continuously decrease, making it immediately noticeable
- **always_on_top**: Whether the window should always stay on top (default: false)
  - If set to `true`, the window will always appear above other windows
  - If set to `false`, it behaves as a normal window
- **hide_on_mouse_proximity**: Whether to move the window to the back when the mouse approaches (default: false)
  - If set to `true`, when the mouse cursor approaches the window, it automatically moves to the back, and returns to the front when the mouse moves away.
  - If set to `false`, this feature is disabled.
  - This feature only works when `always_on_top` is `true`.
- **proximity_distance**: Distance for mouse proximity detection (in pixels, default: 50)
  - The window moves to the back when the mouse cursor enters within this distance from the window.
  - A larger value detects the mouse from further away.
  - A smaller value requires the mouse to be closer to the window to react.
- **regex**: A regular expression pattern to match against window titles (case-insensitive)
- **score**: An integer value to add to the score when the pattern matches (can be negative)
- **description**: A human-readable description displayed in the status area

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
- A status indicating the currently matched pattern or window title
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

### Example 3: Always-on-top mode with automatic send-to-back on mouse proximity
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

With this configuration, the window normally stays on top, but automatically moves to the back when the mouse cursor approaches within 50 pixels, returning to the front when the mouse moves away. It's designed not to interfere with your work.

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

The application consists of several modules:

- **config.py**: Handles TOML configuration loading and management
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
Uses built-in AppleScript. No additional dependencies are required.

### Windows
Works with the built-in Windows API. Install for better compatibility:
```bash
pip install pywin32
```

## License

See the LICENSE file for details.

*Big Brother is watching you. But this time, it's a cat. 🐱*