#!/usr/bin/env python3
"""
Module for downloading audio or video files.

This module provides functionality to download media files from the internet
using specified URLs, handling multiple downloads concurrently when needed.
"""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from pathlib import Path
from typing import Any, Dict

from yt_dlp import YoutubeDL, DownloadError  # type: ignore[attr-defined]

from core.log_manager import log_message
from core.config import PLAYLIST_URLS, DOWNLOAD_DIR, ARCHIVE_FILE
from core.utils import sanitize_filename

# Define our own YDLOpts alias as a dictionary of options.
YDLOpts = Dict[str, Any]

# Ensure the download directory exists.
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)


def download_single_playlist(playlist_url: str) -> None:
    """
    Download a single playlist with metadata and thumbnail embedding using yt-dlp.

    Args:
        playlist_url (str): URL of the playlist to download.
    """
    log_message(f"Starting download: {playlist_url}")

    ydl_opts: YDLOpts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }
        ],
        "write_thumbnail": True,
        "embed_thumbnail": True,
        "embed_metadata": True,
        "outtmpl": f"{DOWNLOAD_DIR}/"
        + sanitize_filename("%(playlist_index)s - %(title)s.%(ext)s"),
        "download_archive": str(ARCHIVE_FILE),
        "quiet": False,
        "noplaylist": False,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
            ydl.download([playlist_url])
        log_message(f"Completed: {playlist_url}")
        os.system(
            f'termux-notification --title "Downloads Completed" '
            f'--content "Successfully Downloaded {playlist_url}!"'
        )
    except DownloadError as e:
        log_message(f"Download failed for {playlist_url} | Error: {e}", level="ERROR")
    except Exception as e:  # pylint: disable=broad-exception-caught
        log_message(f"Unexpected error for {playlist_url} | Error: {e}", level="ERROR")


def download_all_playlists() -> None:
    """
    Download all playlists concurrently with proper error handling.
    """
    log_message("Starting batch playlist download...")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(download_single_playlist, url): url for url in PLAYLIST_URLS
        }
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as exc:  # pylint: disable=broad-exception-caught
                log_message(f"Error downloading {url}: {exc}", level="ERROR")

    log_message("All downloads complete.")
    os.system(
        'termux-notification --title "Downloads Completed" '
        '--content "Successfully Downloaded All Playlists!"'
    )


def main() -> None:
    """Main entry point for the downloader tool."""
    download_all_playlists()


if __name__ == "__main__":
    main()
