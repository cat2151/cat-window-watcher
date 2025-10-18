#!/usr/bin/env python3
"""Entry point when running as python -m src."""

try:
    from .main import main
except ImportError:
    from main import main

if __name__ == "__main__":
    main()
