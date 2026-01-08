#!/usr/bin/env python3
"""Status text formatting module for cat-window-watcher GUI."""

# Maximum window title length before truncation
MAX_WINDOW_TITLE_LENGTH = 40


class StatusFormatter:
    """Formatter for status text display."""

    @staticmethod
    def format_status_text(matched_pattern, window_title, default_score, elapsed_seconds=0, flow_mode_seconds=0):
        """Generate status text based on pattern match and window title.

        Args:
            matched_pattern: Matched pattern dict with 'description' and 'score', or None
            window_title: Current window title string
            default_score: Default score value when no pattern matches
            elapsed_seconds: Elapsed seconds since current window became active (default: 0)
            flow_mode_seconds: Elapsed seconds since flow mode started (default: 0)

        Returns:
            str: Status text to display
        """
        # Format elapsed time - prioritize flow mode time if active
        if flow_mode_seconds > 0:
            elapsed_text = f" [フロー: {flow_mode_seconds}秒]"
        elif elapsed_seconds > 0:
            elapsed_text = f" [{elapsed_seconds}秒]"
        else:
            elapsed_text = ""

        if matched_pattern:
            description = matched_pattern.get("description", "")
            score_delta = matched_pattern.get("score", 0)
            score_sign = "+" if score_delta >= 0 else ""
            return f"{description} ({score_sign}{score_delta}){elapsed_text}"
        else:
            # No match - always show window title to help users configure patterns
            # Show truncated window title
            display_title = StatusFormatter._truncate_title(window_title)

            # Check if default score was applied
            if default_score != 0:
                score_sign = "+" if default_score >= 0 else ""
                score_text = f"({score_sign}{default_score})"
                # Combine window title with default score information
                return (
                    f"No match: {display_title} {score_text}{elapsed_text}"
                    if display_title
                    else f"No match {score_text}{elapsed_text}"
                )
            else:
                return f"{display_title}{elapsed_text}" if display_title else f"Watching...{elapsed_text}"

    @staticmethod
    def _truncate_title(window_title):
        """Truncate window title if it exceeds maximum length.

        Args:
            window_title: Window title to truncate

        Returns:
            str: Truncated window title
        """
        if len(window_title) > MAX_WINDOW_TITLE_LENGTH:
            return window_title[:MAX_WINDOW_TITLE_LENGTH] + "..."
        return window_title
