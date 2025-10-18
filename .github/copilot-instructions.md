# GitHub Copilot Instructions for cat-window-watcher

## Project Overview

cat-window-watcher is a Python-based window monitoring tool that watches for active window changes and performs actions based on window states.

## Code Style and Standards

### Python Style

- Use Python 3.12+ compatible syntax
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include shebang `#!/usr/bin/env python3` at the top of executable scripts
- Support both relative and absolute imports for maximum compatibility:
  ```python
  try:
      from .module import Class
  except ImportError:
      from module import Class
  ```

### Documentation

- Add docstrings to all classes and public methods
- Use triple-quoted strings with clear descriptions
- Include Args, Returns, and Raises sections in docstrings when applicable
- Example format:
  ```python
  def method_name(self, param):
      """Brief description.

      Args:
          param: Description of parameter

      Returns:
          type: Description of return value

      Raises:
          ErrorType: Description of when error is raised
      """
  ```

### Comments

- Add comments to explain complex logic or non-obvious behavior
- Use inline comments sparingly and only when necessary
- Prefer self-documenting code over excessive comments

## Testing

### Test Framework

- Use Python's built-in `unittest` framework for all tests
- Place all test files in the `tests/` directory
- Name test files with prefix `test_` (e.g., `test_feature.py`)
- Use descriptive test method names starting with `test_`

### Test Structure

- Create a test class inheriting from `unittest.TestCase`
- Use `setUp()` for test fixtures
- Use `tearDown()` for cleanup
- Use `tempfile.mkdtemp()` for temporary test directories
- Clean up temporary files after tests

### Test Coverage

- Write tests for all new features and bug fixes
- Include both positive and negative test cases
- Test edge cases and error conditions
- Validate error messages and exception handling

## Configuration

### TOML Configuration

- Use TOML format for all configuration files
- Configuration should support window monitoring settings

## Architecture

### Module Organization

- Keep modules focused on single responsibilities
- Use static methods for utility functions that don't require instance state
- Handle errors gracefully with informative error messages
- Use `print()` for user-facing output and logging

## Error Handling

### Configuration Errors

- Catch `FileNotFoundError` for missing config files
- Catch `toml.TomlDecodeError` for invalid TOML syntax
- Print clear error messages to users
- Exit with `sys.exit(1)` for fatal errors

### Runtime Errors

- Handle `OSError` for file system operations
- Catch general exceptions and provide helpful error messages
- Continue operation when non-fatal errors occur

## Compatibility

### Platform Support

- Support Linux, macOS, and Windows
- Use `os.path` for cross-platform file path handling
- Test platform-specific functionality on multiple platforms

### Python Version

- Maintain compatibility with Python 3.6+
- Use features available in older Python versions when possible
- Document minimum Python version requirements

## Code Formatting and Quality

### Before Committing Changes

**IMPORTANT**: Always run the following commands before committing any Python code changes:

```bash
# Format code with Ruff
ruff format src/ tests/

# Fix auto-fixable lint issues
ruff check --fix src/ tests/

# Verify formatting and linting (should pass with no errors)
ruff format --check src/ tests/
ruff check src/ tests/
```

These steps are **mandatory** for all code changes. Failure to format code will result in:
- PR review delays
- Manual formatting required by maintainers
- Potential PR rejection

### Why This Matters

- The project enforces consistent code style using Ruff
- Manual formatting before commit is the safest and most efficient approach

## Best Practices

- Write self-documenting code with clear variable names
- Keep functions small and focused
- Avoid premature optimization
- Test changes thoroughly before committing
- **Always run ruff format and ruff check before committing**
- Use meaningful commit messages
- Follow existing code patterns and conventions
