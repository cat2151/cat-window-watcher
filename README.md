# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that watches active windows and adjusts your score based on your activity.

<p align="left">
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵-Japanese-red.svg" alt="Japanese"></a>
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸-English-blue.svg" alt="English"></a>
</p>

## WIP

Under development. There are bugs. Please refer to the issues.

## ⚠️ Note on Provisional Implementation

This is a **provisional implementation for testing and validation**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps at this stage)
- Straightforward logic: checks the active window title every second
- Minimal complexity to facilitate rapid development and testing

While future versions may include optimizations and integrations, this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors the currently active window and adjusts a score based on configurable patterns:
- Working on GitHub? Your score goes up! 🎉
- Browsing social media? Your score goes down... 😿

The cat is watching you!

## Features

-   **Simple Score Display**: Shows the current score in a clean tkinter GUI
-   **Regex-based Window Matching**: Configure window title patterns using regular expressions
-   **Configurable Score Values**: Set custom score increments or decrements for each pattern
-   **Cross-Platform Compatibility**: Works on Linux, macOS, and Windows
-   **Lightweight**: Checks window titles once per second, minimal resource usage

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

1.  Clone the repository:
```bash
git clone https://github.com/cat2151/cat-window-watcher.git
cd cat-window-watcher
```

2.  Ensure Python 3.12 or higher is installed:
```bash
python --version
```

3.  Install dependencies (if necessary):
    -   Linux: `xdotool` or `xprop` (usually pre-installed)
    -   macOS: Built-in AppleScript support
    -   Windows: Works with built-in API (optionally use `pywin32` for better support)

## Configuration

1.  Copy the example configuration:
```bash
cp config.toml.example config.toml
```

2.  Edit `config.toml` to customize window patterns and scores:

```toml
# Default score (applied when no pattern matches)
# Used to easily detect misconfigurations
# -1 (default) makes misconfigurations obvious, set to 0 to disable
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

-   **default_score**: Score applied when no pattern matches (default: -1)
    -   Setting to -1 (default) helps in easily verifying if patterns are correctly configured.
    -   Setting to 0 means the score won't change if no pattern matches.
    -   If patterns are misconfigured, the score will continuously decrease, making it immediately noticeable.
-   **regex**: Regular expression pattern to match against the window title (case-insensitive)
-   **score**: Integer value to add to the score when the pattern matches (can be negative)
-   **description**: Human-readable description displayed in the status area

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

The GUI displays:
-   The current score in large text
-   A status indicating the currently matched pattern or window title
-   Automatic updates every second

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

-   **config.py**: Handles loading and managing TOML configurations
-   **window_monitor.py**: Provides cross-platform window title detection
-   **score_tracker.py**: Matches window titles against patterns and tracks the score
-   **gui.py**: tkinter-based interface for displaying the score
-   **main.py**: Application entry point and orchestration

## Platform-Specific Notes

### Linux
`xdotool` or `xprop` is required:
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