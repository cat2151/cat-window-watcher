#!/usr/bin/env python3
"""Configuration validation module for cat-window-watcher."""


class ConfigValidator:
    """Validator for configuration values."""

    @staticmethod
    def validate_hex_color(color_value, color_name):
        """Validate hex color format.

        Args:
            color_value: Color value to validate
            color_name: Name of the color setting (for error messages)

        Raises:
            ValueError: If color format is invalid
        """
        if not isinstance(color_value, str):
            raise ValueError(
                f"Invalid '{color_name}' value: {color_value!r}. Must be a hex color string (e.g., '#ffffff')."
            )
        if not color_value.startswith("#") or len(color_value) != 7:
            raise ValueError(
                f"Invalid '{color_name}' value: {color_value!r}. Must be a 7-character hex color string (e.g., '#ffffff')."
            )
        try:
            # Validate hex digits after '#'
            int(color_value[1:], 16)
        except ValueError:
            raise ValueError(
                f"Invalid '{color_name}' value: {color_value!r}. Must contain valid hex digits after '#' (0-9, a-f)."
            ) from None

    @staticmethod
    def validate_boolean(value, setting_name):
        """Validate boolean value.

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not a boolean
        """
        if not isinstance(value, bool):
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be a boolean.")

    @staticmethod
    def validate_integer(value, setting_name):
        """Validate integer value.

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not an integer
        """
        if not isinstance(value, int):
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be an integer.")

    @staticmethod
    def validate_non_negative_integer(value, setting_name):
        """Validate non-negative integer value.

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not a non-negative integer
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be a non-negative integer.")

    @staticmethod
    def validate_hour(value, setting_name):
        """Validate hour value (0-23).

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not an integer between 0 and 23
        """
        if not isinstance(value, int) or not (0 <= value <= 23):
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be an integer between 0 and 23.")

    @staticmethod
    def validate_transparency(value, setting_name):
        """Validate transparency/opacity value (0.0-1.0).

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not a number between 0.0 and 1.0
        """
        if not isinstance(value, (int, float)):
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be a number (int or float).")
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be between 0.0 and 1.0.")

    @staticmethod
    def validate_percentage(value, setting_name):
        """Validate percentage value (1-100).

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not an integer between 1 and 100
        """
        if not isinstance(value, int) or value <= 0 or value > 100:
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be an integer between 1 and 100.")

    @staticmethod
    def validate_optional_integer(value, setting_name):
        """Validate optional integer value (can be None).

        Args:
            value: Value to validate
            setting_name: Name of the setting (for error messages)

        Raises:
            ValueError: If value is not None and not an integer
        """
        if value is not None and not isinstance(value, int):
            raise ValueError(f"Invalid '{setting_name}' value: {value!r}. Must be an integer or null.")
