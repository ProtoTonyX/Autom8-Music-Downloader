import os
import pytest
from core.downloader import download_single_playlist, download_all_playlists
from yt_dlp import DownloadError


# Dummy YoutubeDL that simulates download behavior.
class DummyYoutubeDL:
    def __init__(self, opts):
        self.opts = opts
        self.download_called = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        pass

    def download(self, urls):
        self.download_called = True
        # If the URL contains "fail", simulate a failure.
        if any("fail" in url for url in urls):
            raise DownloadError("Simulated download failure")
        # Otherwise, simulate a successful download.
        return


# Patch YoutubeDL in the downloader module.
@pytest.fixture(autouse=True)
def patch_youtubedl(monkeypatch):
    monkeypatch.setattr("core.downloader.YoutubeDL", DummyYoutubeDL)


# Capture os.system calls.
@pytest.fixture(autouse=True)
def patch_os_system(monkeypatch):
    calls = []

    def fake_system(cmd):
        calls.append(cmd)
        return 0

    monkeypatch.setattr(os, "system", fake_system)
    return calls


# Capture log messages.
@pytest.fixture
def captured_logs(monkeypatch):
    logs = []

    def fake_log(message, level="INFO"):
        logs.append((level, message))

    monkeypatch.setattr("core.downloader.log_message", fake_log)
    return logs


# Override configuration values with temporary ones.
@pytest.fixture
def dummy_config(monkeypatch, tmp_path):
    dummy_download_dir = tmp_path / "downloads"
    dummy_download_dir.mkdir()
    dummy_archive = tmp_path / "archive.txt"
    # Use two test URLs: one that should succeed, one that simulates failure.
    test_urls = [
        "http://example.com/playlist_success",
        "http://example.com/fail_playlist",
    ]
    monkeypatch.setattr("core.downloader.DOWNLOAD_DIR", str(dummy_download_dir))
    monkeypatch.setattr("core.downloader.ARCHIVE_FILE", dummy_archive)
    monkeypatch.setattr("core.downloader.PLAYLIST_URLS", test_urls)
    return dummy_download_dir, dummy_archive, test_urls


def test_download_single_playlist_success(captured_logs, patch_os_system):
    """Test that a successful download logs start and completion."""
    test_url = "http://example.com/playlist_success"
    download_single_playlist(test_url)
    # Check that logs include the starting and completed messages.
    start_logged = any("Starting download" in msg for _, msg in captured_logs)
    complete_logged = any("Completed" in msg for _, msg in captured_logs)
    assert start_logged, "Download did not log starting message"
    assert complete_logged, "Download did not log completion message"


def test_download_single_playlist_failure(captured_logs, patch_os_system):
    """Test that a failed download logs an error message."""
    test_url = "http://example.com/fail_playlist"
    download_single_playlist(test_url)
    error_logged = any("Download failed" in msg for _, msg in captured_logs)
    assert error_logged, "Download failure was not logged"


def test_download_all_playlists(dummy_config, captured_logs, patch_os_system):
    """Test that download_all_playlists processes all URLs concurrently."""
    download_all_playlists()
    # We expect one success and one failure based on our test URLs.
    success_logged = any("Completed" in msg for _, msg in captured_logs)
    failure_logged = any("Download failed" in msg for _, msg in captured_logs)
    assert success_logged, "Expected a successful download log"
    assert failure_logged, "Expected a failed download log"
