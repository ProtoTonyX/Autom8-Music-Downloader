#!/usr/bin/env python3

"""Script for running the sync operation.

This script manages the synchronization of music files from the source
directory to the destination directory, ensuring that files are up-to-date
and accurately reflected in both locations.
"""

import signal
import sys
from core.sync_manager import sync_music
from core.log_manager import log_message


def handle_sigint(_sig, _frame):
    """Handles Ctrl+C interrupt for graceful shutdown."""
    log_message("Sync interrupted. Exiting gracefully...", level="INFO")
    sys.exit(0)


# Attach SIGINT handler
signal.signal(signal.SIGINT, handle_sigint)

if __name__ == "__main__":
    try:
        sync_music()
    except KeyboardInterrupt:
        log_message("Sync interrupted by user.", level="WARNING")
        sys.exit(0)
