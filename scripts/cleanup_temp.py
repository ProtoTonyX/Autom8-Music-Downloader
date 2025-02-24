#!/usr/bin/env python3

"""Script for cleaning up temporary download files.

This script scans for and removes temporary files that were created
during the download process, helping to free up disk space.
"""

from core.cleanup import run_cleanup
from core.log_manager import log_message

if __name__ == "__main__":
    log_message("Starting cleanup process...")
    run_cleanup()
    log_message("Cleanup complete!")
