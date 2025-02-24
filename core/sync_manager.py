#!/usr/bin/env python3

"""Module for syncing media files.

This module handles the synchronization of media files between different
locations, ensuring that files are kept up-to-date and in the correct
directories.
"""

from pathlib import Path
import shutil
from core.config import DOWNLOAD_DIR, MUSIC_DIR, DEFAULT_THUMBNAIL, AUDIO_FORMAT
from core.log_manager import log_message
from core.utils import embed_thumbnail


def collect_audio_files() -> list[Path]:
    """Collects all downloaded audio files and logs them."""
    files = list(DOWNLOAD_DIR.glob("*.*"))  # Get all files first
    log_message(
        f"DEBUG: Found {len(files)} total files: {[f.name for f in files]}", "INFO"
    )

    audio_files = [f for f in files if f.suffix == f".{AUDIO_FORMAT}"]

    if not audio_files:
        log_message(
            "⚠️ No matching audio files found! Check filename formats.", "WARNING"
        )

    return audio_files


def sync_music() -> None:
    """Syncs downloaded music to the music directory, ensuring thumbnails are embedded."""
    log_message(f"Starting sync: {DOWNLOAD_DIR} → {MUSIC_DIR}")

    if not MUSIC_DIR.exists():
        log_message(f"Music directory not found: {MUSIC_DIR}", level="ERROR")
        return

    files_to_sync = collect_audio_files()
    if not files_to_sync:
        log_message("No new music to sync.", level="INFO")
        return

    for file in files_to_sync:
        try:
            # 🔹 Embed thumbnail *before* copying
            embed_thumbnail(file, DEFAULT_THUMBNAIL, file)

            destination = MUSIC_DIR / file.name
            shutil.copy2(file, destination)
            log_message(f"Copied: {file} → {destination}")

        except (OSError, shutil.Error) as e:
            log_message(f"Failed to sync {file}: {e}", level="ERROR")


if __name__ == "__main__":
    sync_music()
