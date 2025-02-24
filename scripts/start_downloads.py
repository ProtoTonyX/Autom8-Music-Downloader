#!/usr/bin/env python3

"""Script for initiating download processes.

This script triggers the download of specified audio or video files from
urls provided in a configuration file or user input.
"""

import signal
import sys
from core.downloader import download_all_playlists
from core.dependencies import verify_dependencies
from core.log_manager import log_message


def handle_sigint(_sig, _frame):
    """Handles Ctrl+C interrupt for graceful shutdown."""
    log_message("Download interrupted. Exiting gracefully...", level="INFO")
    sys.exit(0)


# Attach SIGINT handler
signal.signal(signal.SIGINT, handle_sigint)

if __name__ == "__main__":
    try:
        verify_dependencies()  # Ensure required commands exist
        download_all_playlists()
    except KeyboardInterrupt:
        log_message("Process interrupted by user.", level="WARNING")
        sys.exit(0)
