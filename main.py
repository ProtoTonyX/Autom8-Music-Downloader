#!/usr/bin/env python3

"""Main entry point for the Music Sync Tool application.

This script initializes the application, sets up necessary configurations,
and executes the synchronization of music files between specified locations.
"""

import sys
from core.downloader import download_all_playlists
from core.sync_manager import sync_music
from core.cleanup import run_cleanup
from core.log_manager import log_message
from core.dependencies import verify_dependencies


def main():
    """Main function to execute the Music Sync Tool.

    This function coordinates the synchronization process, handles user
    inputs, and manages the application workflow.
    """
    print("\n🎵 Music Sync Tool 🎵")
    print("1. Download Playlists")
    print("2. Sync Music")
    print("3. Cleanup Temporary Files")
    print("4. Verify Dependencies")
    print("5. Exit")

    choice = input("\nEnter a number: ").strip()

    if choice == "1":
        log_message("Starting playlist download...")
        download_all_playlists()
    elif choice == "2":
        log_message("Starting music sync...")
        sync_music()
    elif choice == "3":
        log_message("Running cleanup process...")
        run_cleanup()
    elif choice == "4":
        log_message("Checking system dependencies...")
        verify_dependencies()
    elif choice == "5":
        print("Exiting.")
        sys.exit(0)
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    while True:
        main()
