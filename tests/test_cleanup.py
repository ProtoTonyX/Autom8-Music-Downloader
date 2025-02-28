import pytest
from pathlib import Path
from core.cleanup import remove_temp_files

TEST_DOWNLOADS = Path("tests/test_downloads")


@pytest.fixture(scope="module", autouse=True)
def setup_real_temp_files():
    """Setup: Create real temp files for cleanup testing."""
    temp_file = TEST_DOWNLOADS / "song_temp.m4a"
    temp_file.touch()  # Create an empty file

    yield  # Run tests

    # Cleanup after tests
    temp_file.unlink(missing_ok=True)


def test_remove_temp_files(monkeypatch):
    """Ensure remove_temp_files deletes real temp files."""
    monkeypatch.setattr("core.config.DOWNLOAD_DIR", TEST_DOWNLOADS)

    temp_file = TEST_DOWNLOADS / "song_temp.m4a"
    assert temp_file.exists(), "Temp file was missing before test!"

    remove_temp_files()

    assert not temp_file.exists(), "Temp file was not deleted!"
