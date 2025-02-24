#!/usr/bin/env python3

"""Module for configuration settings.

This module contains configuration settings and constants used throughout
the application, such as download directories and audio formats.
"""

from pathlib import Path  # Keep this import

# === DIRECTORY CONFIGURATION ===
BASE_DIR = Path.home() / "Workspace/music_sync_tool"
DOWNLOAD_DIR = BASE_DIR / "downloads"
LOG_DIR = BASE_DIR / ".logs"
MUSIC_DIR = Path("/storage/emulated/0/Music")  # Android Music Folder
ARCHIVE_FILE = LOG_DIR / "downloaded_songs.txt"

# Ensure required directories exist
for path in [DOWNLOAD_DIR, LOG_DIR]:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass  # The directory already exists, which we expect.
    except OSError as e:  # Catch specific exceptions
        print(f"Error creating directory {path}: {e}")

# === DOWNLOAD SETTINGS ===
AUDIO_FORMAT = "m4a"
THUMBNAIL_FORMAT = "png"

# === PERFORMANCE SETTINGS ===
CONCURRENT_DOWNLOADS = 5
MAX_LOG_SIZE_MB = 1

# === REQUIRED COMMANDS ===
REQUIRED_COMMANDS = ["yt-dlp", "ffmpeg", "termux-wake-lock", "termux-wake-unlock", "am"]

# === PLAYLIST CONFIGURATION ===
PLAYLIST_URLS = [
    "https://youtube.com/playlist?list=PL8Q_6ustbCvHG9zEz8Z0hnrQYzWIAHpvl&si=XCJBwLkW6BwlAMHq",
    "https://youtube.com/playlist?list=PL8Q_6ustbCvFeHcMXb0cSzGoDIowblg4s&si=zDabgDPdj51bPUgt",
    "https://youtube.com/playlist?list=PL8Q_6ustbCvGY1aNJm9g_IkG4-puFkvqt&si=l-OkBh_1kYz1MOTC",
    "https://youtube.com/playlist?list=PL8Q_6ustbCvFIrCpkKXPtBKUUusOZtPUZ&si=40TrAeYduwJXwRs-",
    "https://youtube.com/playlist?list=PL8Q_6ustbCvFI0QpKeZ7GuwCnaFmOeW24&si=gJKlAUZo16cM8quH",
    "https://youtube.com/playlist?list=PL8Q_6ustbCvHD-j_WWtuP2cIfCk8MKY-1&si=3lx8_pVKD01JZIfj",
]

# === DEFAULT THUMBNAIL ===
DEFAULT_THUMBNAIL = (
    Path.home() / "Workspace/music_sync_tool/.DigiArt/default_thumb_starryai.png"
)

# Check if the default thumbnail exists
if not DEFAULT_THUMBNAIL.exists():
    print(
        f"Warning: Default thumbnail not found at {DEFAULT_THUMBNAIL}. Please ensure it exists."
    )
