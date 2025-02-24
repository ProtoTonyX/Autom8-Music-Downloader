#!/usr/bin/env python3

"""Utility functions for the application.

This module contains various helper functions that are used throughout the
application for tasks such as generating file hashes, triggering media scans
for Android devices, and embedding thumbnails in audio files.

Functions:
- generate_file_hash(file_path: Path) -> str: Generates an MD5 hash for a given file.
- trigger_media_scan(file_path: Path) -> None: Initiates a media scan on an Android device
  to register new media files.
- embed_thumbnail(audio_file: Path, thumbnail_file: Path, output_file: Path) -> None:
  Embeds a thumbnail image into an audio file using ffmpeg.

Usage:
Import this module where utility functions are needed and call the desired function
with the appropriate parameters.

Exceptions:
Each function in this module may log errors related to file handling or subprocess
execution failures, providing feedback on any issues encountered.
"""

import hashlib
import subprocess
from pathlib import Path
from core.log_manager import log_message


def generate_file_hash(file_path: Path) -> str:
    """Generate an MD5 hash for a file (useful for duplicate detection)."""
    hash_md5 = hashlib.md5()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def trigger_media_scan(file_path: Path) -> None:
    """Force Android to recognize new media files."""
    try:
        subprocess.run(
            [
                "am",
                "broadcast",
                "-a",
                "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
                "-d",
                f"file://{file_path}",
            ],
            check=True,
        )
        log_message(f"Triggered media scan for: {file_path}")
    except subprocess.CalledProcessError as e:
        log_message(f"Media scan failed for {file_path}: {e}", "ERROR")


def embed_thumbnail(audio_file: Path, thumbnail_file: Path, output_file: Path) -> None:
    """Embeds the default thumbnail into the audio file using ffmpeg."""
    command = [
        "ffmpeg",
        "-i",
        str(audio_file),
        "-i",
        str(thumbnail_file),
        "-map",
        "0",
        "-map",
        "1",
        "-c",
        "copy",
        "-disposition:v",
        "attached_pic",
        str(output_file),
        "-y",
    ]

    try:
        subprocess.run(command, check=True)
        log_message(f"✅ Thumbnail embedded: {audio_file}")
    except subprocess.CalledProcessError as e:
        log_message(
            f"❌ Thumbnail embed failed for {audio_file}\nError: {e.stderr}",
            level="ERROR",
        )
