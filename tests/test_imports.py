def test_import_cleanup():
    from core import cleanup

    assert hasattr(cleanup, "remove_temp_files"), "cleanup.remove_temp_files not found"
    assert hasattr(cleanup, "embed_default_thumbnail"), (
        "cleanup.embed_default_thumbnail not found"
    )
    assert hasattr(cleanup, "run_cleanup"), "cleanup.run_cleanup not found"


def test_import_downloader():
    from core import downloader

    assert hasattr(downloader, "download_single_playlist"), (
        "downloader.download_single_playlist not found"
    )
    assert hasattr(downloader, "download_all_playlists"), (
        "downloader.download_all_playlists not found"
    )
    assert hasattr(downloader, "main"), "downloader.main not found"


def test_import_sync_manager():
    from core import sync_manager

    assert hasattr(sync_manager, "collect_audio_files"), (
        "sync_manager.collect_audio_files not found"
    )
    assert hasattr(sync_manager, "sync_music"), "sync_manager.sync_music not found"


def test_import_utils():
    from core import utils

    assert hasattr(utils, "generate_file_hash"), "utils.generate_file_hash not found"
    assert hasattr(utils, "trigger_media_scan"), "utils.trigger_media_scan not found"
    assert hasattr(utils, "embed_thumbnail"), "utils.embed_thumbnail not found"
    assert hasattr(utils, "sanitize_filename"), "utils.sanitize_filename not found"


def test_import_config():
    from core import config

    expected_attrs = [
        "PLAYLIST_URLS",
        "DOWNLOAD_DIR",
        "ARCHIVE_FILE",
        "MUSIC_DIR",
        "DEFAULT_THUMBNAIL",
        "AUDIO_FORMAT",
    ]
    for attr in expected_attrs:
        assert hasattr(config, attr), f"config.{attr} not found"


def test_import_log_manager():
    from core import log_manager

    assert hasattr(log_manager, "log_message"), "log_manager.log_message not found"
