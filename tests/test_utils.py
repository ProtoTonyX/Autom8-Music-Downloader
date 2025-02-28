import pytest
from pathlib import Path
from core.utils import generate_file_hash, embed_thumbnail
import shutil

# Use real test files
TEST_DOWNLOADS = Path("tests/test_downloads")
TEST_OUTPUT_DIR = Path("tests/test_output")


@pytest.fixture(scope="module", autouse=True)
def setup_test_files():
    """Ensure test directories exist and contain real `.m4a` files."""
    TEST_OUTPUT_DIR.mkdir(exist_ok=True)

    sample_audio = TEST_DOWNLOADS / "sample.m4a"
    sample_thumb = TEST_DOWNLOADS / "sample.png"

    # Ensure real files exist
    assert sample_audio.exists(), "No test .m4a file found!"
    assert sample_thumb.exists(), "No test thumbnail found!"

    yield  # Run tests

    # Cleanup generated files
    shutil.rmtree(TEST_OUTPUT_DIR, ignore_errors=True)


@pytest.fixture
def create_test_file(tmp_path):
    """Creates a fake test file for hashing."""
    file = tmp_path / "test.txt"
    file.write_text("some data")
    return file


def test_generate_file_hash(create_test_file):
    """Ensure generate_file_hash produces a hash string."""
    file = create_test_file
    file_hash = generate_file_hash(file)

    assert isinstance(file_hash, str)
    assert len(file_hash) == 32  # MD5 hashes are 32 chars long


def test_embed_thumbnail():
    """Ensure embed_thumbnail actually processes a real audio file."""
    audio_file = TEST_DOWNLOADS / "sample.m4a"
    thumb_file = TEST_DOWNLOADS / "sample.png"
    output_file = TEST_OUTPUT_DIR / "output.m4a"

    embed_thumbnail(audio_file, thumb_file, output_file)

    assert output_file.exists(), "FFmpeg did not generate output!"
