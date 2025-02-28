import pytest
from pathlib import Path
import shutil
from core.sync_manager import collect_audio_files, sync_music

# Use real test files
TEST_DOWNLOADS = Path("tests/test_downloads")  # ✅ Use real directory
TEST_MUSIC_DIR = Path("tests/test_music_output")  # Temporary music dir


@pytest.fixture(scope="module", autouse=True)
def setup_real_files():
    """Setup: Ensure test directories exist and contain real `.m4a` files."""
    TEST_MUSIC_DIR.mkdir(exist_ok=True)  # Ensure output dir exists

    # Ensure we have real .m4a files
    assert any(TEST_DOWNLOADS.glob("*.m4a")), "No .m4a test files found!"

    yield  # Run tests

    # Cleanup after tests
    shutil.rmtree(TEST_MUSIC_DIR, ignore_errors=True)


def test_collect_audio_files(monkeypatch):
    """Ensure collect_audio_files finds real .m4a files."""
    monkeypatch.setattr("core.config.DOWNLOAD_DIR", TEST_DOWNLOADS)

    found_files = collect_audio_files()
    assert len(found_files) > 0, "No audio files found!"
    assert all(f.suffix == ".m4a" for f in found_files), "Non-m4a files found!"


def test_sync_music(monkeypatch):
    """Ensure sync_music copies real files correctly."""
    monkeypatch.setattr("core.config.DOWNLOAD_DIR", TEST_DOWNLOADS)
    monkeypatch.setattr("core.config.MUSIC_DIR", TEST_MUSIC_DIR)

    sync_music()

    # Ensure all files were copied
    for file in TEST_DOWNLOADS.glob("*.m4a"):
        assert (TEST_MUSIC_DIR / file.name).exists(), f"{file.name} was not copied!"
