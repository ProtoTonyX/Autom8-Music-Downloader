#!/usr/bin/env python3

"""Module for logging application events.

This module provides functionality to log important events and messages
generated during the runtime of the application, aiding in debugging and
monitoring.
"""

import logging
from core.config import LOG_DIR

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# Setup logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)


def log_message(message: str, level: str = "INFO") -> None:
    """Logs a message with the specified level."""
    level = level.upper()  # Ensure level is uppercase
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
    else:
        logging.debug(message)

    # Print to console with formatting
    print(f"[{level}] {message}")
