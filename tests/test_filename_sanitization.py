import pytest
from core.utils import sanitize_filename


@pytest.mark.parametrize(
    "raw,expected_substr",
    [
        # Given raw filenames with quotes and escapes, we expect the sanitized version to have them removed.
        ('"001 - Ain\'t Too Hard.m4a"', "001 - Ain't Too Hard.m4a"),
        ("'01 - Keep Faith.m4a'", "01 - Keep Faith.m4a"),
        ("'01 - Feel Like a Rapper.m4a'", "01 - Feel Like a Rapper.m4a"),
        # Test a case with escape characters and invalid symbols.
        ("\\001 - Example?.m4a", "001 - Example_.m4a"),
    ],
)
def test_sanitize_filename(raw, expected_substr):
    sanitized = sanitize_filename(raw)
    # Assert that the sanitized filename contains the expected substring.
    # (This isn't a strict equality check, because you might want to allow for minor differences,
    # as long as quotes/escapes are removed.)
    assert expected_substr in sanitized, (
        f"Sanitized filename '{sanitized}' does not contain expected substring '{expected_substr}'"
    )
    # Also assert that no extraneous quotes remain.
    assert '"' not in sanitized and "'" not in sanitized, (
        f"Sanitized filename '{sanitized}' should not contain quotes."
    )


def test_downloader_outtmpl_integration(monkeypatch):
    """
    This test simulates the downloader's use of sanitize_filename in its outtmpl option.
    It verifies that the constructed template does not include unwanted characters.
    """
    from core.config import (
        DOWNLOAD_DIR,
    )  # assuming DOWNLOAD_DIR is a simple string path
    from core.downloader import (
        download_single_playlist,
    )  # to trigger the outtmpl construction

    # Capture the options that would be passed to YoutubeDL.
    captured_opts = {}

    class DummyYDLOpts:
        def __init__(self, opts):
            self.opts = opts

        def __enter__(self):
            # Capture the outtmpl for inspection.
            nonlocal captured_opts
            captured_opts = self.opts
            return self

        def __exit__(self, exc_type, exc_val, traceback):
            pass

        def download(self, urls):
            # Do nothing—this is just to simulate the download process.
            return

    # Monkey-patch YoutubeDL in the downloader to use our dummy.
    monkeypatch.setattr("core.downloader.YoutubeDL", DummyYDLOpts)

    # Trigger a download with a dummy URL.
    test_url = "http://example.com/playlist_success"
    download_single_playlist(test_url)

    # Now, inspect the outtmpl in the options.
    outtmpl = captured_opts.get("outtmpl", "")
    # Assert that it doesn't include extraneous quotes.
    assert '"' not in outtmpl and "'" not in outtmpl, (
        f"Output template '{outtmpl}' should not contain quotes."
    )
    # You can also check that it starts with the expected DOWNLOAD_DIR and ends with the proper extension.
    assert outtmpl.startswith(DOWNLOAD_DIR), (
        f"Output template '{outtmpl}' should start with the DOWNLOAD_DIR '{DOWNLOAD_DIR}'."
    )
    assert outtmpl.endswith(".m4a"), (
        f"Output template '{outtmpl}' should end with '.m4a'."
    )
