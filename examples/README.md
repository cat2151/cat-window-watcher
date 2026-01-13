# Configuration Examples

This directory contains example configuration files for cat-window-watcher. Each example demonstrates different use cases and configuration patterns.

## Available Examples

### Example 1: Tracking Productivity
- **English**: [example1_productivity.toml](example1_productivity.toml)
- **Japanese**: [example1_productivity.ja.toml](example1_productivity.ja.toml)

Tracks productivity by monitoring work-related windows (GitHub, GitLab) vs social media.

### Example 2: Study Time
- **English**: [example2_study_time.toml](example2_study_time.toml)
- **Japanese**: [example2_study_time.ja.toml](example2_study_time.ja.toml)

Helps track study and reading time (PDFs, documentation) vs entertainment (YouTube, Netflix).

### Example 3: Always-on-top Mode with Mouse Proximity Hide
- **English**: [example3_always_on_top.toml](example3_always_on_top.toml)
- **Japanese**: [example3_always_on_top.ja.toml](example3_always_on_top.ja.toml)

Demonstrates the always-on-top feature with automatic hide when mouse approaches the window.

## Using an Example

To use an example configuration:

```bash
# Copy an example to config.toml
cp examples/example1_productivity.toml config.toml

# Or run directly with a specific example
python src/main.py --config examples/example1_productivity.toml
```

## Creating Your Own Configuration

Use these examples as starting points for your own configuration. You can combine features from different examples or create entirely new patterns based on your needs.

For more information about configuration options, see the main [README.md](../README.md) or [README.ja.md](../README.ja.md).
