# Cat Window Watcher - Usage Guide

## Quick Start

1. **Create your configuration file:**
   ```bash
   cp config.toml.example config.toml
   ```

2. **Edit the configuration** to match your needs:
   ```bash
   nano config.toml  # or your preferred editor
   ```

3. **Run the application:**
   ```bash
   python src/main.py
   ```

## Understanding the Configuration

The configuration file uses TOML format with window patterns that define:
- **regex**: Pattern to match window titles (case-insensitive)
- **score**: Points to add when this window is active (can be negative)
- **description**: Human-readable name shown in the GUI

### Example Pattern

```toml
[[window_patterns]]
regex = "github"           # Matches any window with "github" in the title
score = 10                 # Adds 10 points to your score
description = "GitHub"     # Shows "GitHub" in the status
```

## Understanding the GUI

The application window displays:

```
╔════════════════════════════════════════╗
║  Cat Window Watcher                    ║
║  - Cat is watching you -               ║
╠════════════════════════════════════════╣
║                                        ║
║           Score: 42                    ║
║                                        ║
║          GitHub (+10)                  ║
║                                        ║
╚════════════════════════════════════════╝
```

- **Score**: Your current score (cumulative)
- **Status**: Shows the matched pattern or current window title

## How It Works

1. **Every 1 second**, the application checks your active window title
2. **If the title changes**, it compares it against your configured patterns
3. **When a pattern matches**, the score is updated by the pattern's value
4. **Only the first matching pattern** is applied for each window change

## Common Use Cases

### 1. Productivity Tracking

Track time spent on work vs. distractions:

```toml
# Work applications (increase score)
[[window_patterns]]
regex = "github|gitlab"
score = 10
description = "Code Repository"

[[window_patterns]]
regex = "vscode|visual studio|intellij|pycharm"
score = 8
description = "IDE"

[[window_patterns]]
regex = "terminal|bash|powershell"
score = 5
description = "Terminal"

# Distractions (decrease score)
[[window_patterns]]
regex = "twitter|facebook|instagram|reddit"
score = -5
description = "Social Media"

[[window_patterns]]
regex = "youtube|netflix|twitch"
score = -10
description = "Streaming"
```

### 2. Study Time Monitoring

Encourage reading documentation and discourage entertainment:

```toml
[[window_patterns]]
regex = "pdf|documentation|docs|mdn|stackoverflow"
score = 10
description = "Learning"

[[window_patterns]]
regex = "youtube|netflix"
score = -15
description = "Entertainment"

[[window_patterns]]
regex = "games|steam|epic"
score = -20
description = "Gaming"
```

### 3. Language Learning

Track time in language learning apps:

```toml
[[window_patterns]]
regex = "duolingo|babbel|rosetta"
score = 15
description = "Language Practice"

[[window_patterns]]
regex = "anki|memrise"
score = 12
description = "Flashcards"
```

## Tips for Effective Patterns

### 1. Use Specific Patterns First

Patterns are checked in order. Put more specific patterns before general ones:

```toml
# ✓ Good - specific pattern first
[[window_patterns]]
regex = "github\\.com"
score = 10

[[window_patterns]]
regex = "git"
score = 5

# ✗ Bad - general pattern will always match first
[[window_patterns]]
regex = "git"
score = 5

[[window_patterns]]
regex = "github\\.com"
score = 10  # This will never be reached!
```

### 2. Use Pipe (|) for Alternatives

Match multiple similar sites in one pattern:

```toml
[[window_patterns]]
regex = "twitter|x\\.com|facebook|instagram"
score = -5
description = "Social Media"
```

### 3. Escape Special Characters

Some characters have special meaning in regex. Escape them with `\`:

- `.` (dot) → `\\.` (matches literal dot)
- `+` (plus) → `\\+`
- `?` (question) → `\\?`
- `*` (asterisk) → `\\*`

```toml
[[window_patterns]]
regex = "example\\.com"  # Matches example.com
score = 5
```

### 4. Case-Insensitive Matching

All patterns are case-insensitive, so these are equivalent:

```toml
regex = "github"      # Matches: github, GitHub, GITHUB, GiThUb
regex = "GitHub"      # Same as above
regex = "GITHUB"      # Same as above
```

## Troubleshooting

### No Window Title Detected

**Linux:**
```bash
# Install xdotool
sudo apt-get install xdotool
```

**macOS:**
- Grant Terminal/iTerm accessibility permissions in System Preferences → Security & Privacy → Privacy → Accessibility

**Windows:**
```bash
# Optionally install pywin32 for better support
pip install pywin32
```

### Configuration Errors

If you see an error loading the config:

1. Check the TOML syntax is valid
2. Ensure all required fields (regex, score) are present
3. Verify file encoding is UTF-8
4. Check for typos in the file path

### Pattern Not Matching

Test your regex pattern:

```python
import re
pattern = "your_pattern_here"
title = "Your Window Title"
if re.search(pattern, title, re.IGNORECASE):
    print("Match!")
else:
    print("No match")
```

## Advanced Usage

### Running with Custom Config

```bash
python src/main.py --config my_custom_config.toml
```

### Multiple Profiles

Create different config files for different scenarios:

```bash
# Work mode
python src/main.py --config config_work.toml

# Study mode
python src/main.py --config config_study.toml

# Relaxation mode
python src/main.py --config config_relax.toml
```

### Monitoring Your Score

Watch your score throughout the day to understand your habits:

- **Positive score**: Productive day! 🎉
- **Negative score**: Time to refocus 😿
- **Zero score**: Balanced or inactive

## Privacy Note

This application:
- ✓ Runs entirely locally on your machine
- ✓ Does not send any data to external servers
- ✓ Only reads window titles (not content)
- ✓ Does not record or store window history
- ✓ Is open source and auditable

## Next Steps

1. Start with the example configuration
2. Run the app and watch your score
3. Adjust patterns and scores based on your goals
4. Create multiple profiles for different contexts
5. Share your configuration strategies with the community!

---

Remember: The cat is watching you! 🐱
