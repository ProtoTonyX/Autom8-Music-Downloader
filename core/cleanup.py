#!/usr/bin/env python3

"""Module for cleaning up old downloads and temporary files.

This module provides functions to delete files that are no longer needed,
helping to maintain a tidy file system and free up space.
"""

from core.log_manager import log_message
from core.config import DOWNLOAD_DIR, DEFAULT_THUMBNAIL
from core.utils import embed_thumbnail


def remove_temp_files() -> None:
    """Logs temp files before deleting them."""
    temp_files = list(DOWNLOAD_DIR.glob("*_temp.m4a"))

    if not temp_files:
        log_message("No orphaned temp files found.", "INFO")
    else:
        log_message(
            f"🛑 Fnd {len(temp_files)} tmp files bfor dletn: {[f.name for f in temp_files]}"
        )

    for temp_file in temp_files:
        log_message(f"🗑️ Removing temp file: {temp_file}")
        temp_file.unlink(missing_ok=True)


def embed_default_thumbnail() -> None:
    """Ensures all audio files have a thumbnail, embedding the default one if needed."""
    for audio_file in DOWNLOAD_DIR.glob("*.m4a"):
        thumbnail = audio_file.with_suffix(".png")
        if not thumbnail.exists():
            log_message(f"Embedding default thumbnail for: {audio_file}", "WARNING")
            temp_file = audio_file.with_stem(audio_file.stem + "_temp")
            embed_thumbnail(
                audio_file, DEFAULT_THUMBNAIL, temp_file
            )  # Use the new utility func


def run_cleanup() -> None:
    """Runs all cleanup operations."""
    log_message("Starting cleanup process...")
    remove_temp_files()
    embed_default_thumbnail()
    log_message("Cleanup process completed.")


if __name__ == "__main__":
    run_cleanup()
