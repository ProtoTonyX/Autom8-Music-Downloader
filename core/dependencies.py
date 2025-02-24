#!/usr/bin/env python3

"""Module for managing application dependencies.

This module handles the installation and management of necessary third-party
libraries required for the application to function properly.
"""

import shutil
from core.log_manager import log_message
from core.config import REQUIRED_COMMANDS


def ensure_command_exists(command: str) -> None:
    """Check if a required command is installed."""
    if not shutil.which(command):
        log_message(
            f"Missing cmd: {command}. Install it before running the script!",
            "ERROR",
        )
        raise FileNotFoundError(f"{command} is required but not found.")


def verify_dependencies() -> None:
    """Ensure all necessary commands are available before proceeding."""
    log_message("Checking system dependencies...")
    for command in REQUIRED_COMMANDS:
        ensure_command_exists(command)
    log_message("All dependencies verified successfully!")


if __name__ == "__main__":
    verify_dependencies()
