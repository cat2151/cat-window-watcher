# cat-window-watcher - Cat is watching you -

A simple, standalone window monitoring tool that tracks your active window and adjusts a score based on what you're doing.

## ⚠️ Provisional Implementation Notice

This is a **provisional implementation for testing and verification purposes**. The current implementation focuses on:
- Simple, standalone operation (no integration with other apps in this phase)
- Straightforward logic: checks active window title every 1 second
- Minimal complexity to facilitate rapid development and testing

Future versions may include optimizations and integrations, but this version prioritizes simplicity and ease of understanding.

## Concept

The application monitors which window is currently active and adjusts a score based on configurable patterns:
- Working on GitHub? Score increases! 🎉
- Browsing social media? Score decreases... 😿

The cat is watching you!

## Features

- **Simple Score Display**: Shows your current score in a clean tkinter GUI
- **Regex-based Window Matching**: Configure window title patterns using regular expressions
- **Configurable Score Values**: Set custom score increase/decrease amounts for each pattern
- **Cross-platform Support**: Works on Linux, macOS, and Windows
- **Lightweight**: Checks window title once per second, minimal resource usage

## What It Looks Like

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

The GUI features a dark theme with a large score display and status showing your current activity.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cat2151/cat-window-watcher.git
cd cat-window-watcher
```

2. Ensure you have Python 3.12+ installed:
```bash
python --version
```

3. Install dependencies (if needed):
   - Linux: `xdotool` or `xprop` (usually pre-installed)
   - macOS: Built-in AppleScript support
   - Windows: Works with built-in APIs (optional: `pywin32` for better support)

## Configuration

1. Copy the example configuration:
```bash
cp config.toml.example config.toml
```

2. Edit `config.toml` to customize window patterns and scores:

```toml
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

- **regex**: Regular expression pattern to match against window titles (case-insensitive)
- **score**: Integer value to add to score when pattern matches (can be negative)
- **description**: Human-readable description shown in the status area

## Usage

Run the application:
```bash
# Method 1: Direct script execution
python src/main.py

# Method 2: Run as module
python -m src

# Method 3: With custom config file
python src/main.py --config my_config.toml
python src/main.py -c my_config.toml
```

The GUI will display:
- Current score in large text
- Status showing the current matched pattern or window title
- Updates every second automatically

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
Verify code quality:
```bash
ruff format --check src/ tests/
ruff check src/ tests/
```

## Architecture

The application consists of several modules:

- **config.py**: Loads and manages TOML configuration
- **window_monitor.py**: Cross-platform window title detection
- **score_tracker.py**: Matches window titles against patterns and tracks score
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
Works with built-in Windows APIs. For better compatibility, install:
```bash
pip install pywin32
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure code follows the project style:
1. Run `ruff format` and `ruff check` before committing
2. Add tests for new features
3. Update documentation as needed

---

*Big Brother is watching you. But this time, it's a cat. 🐱*