from kasandra import __version__
from kasandra.config.paths import SQL_DIR, VAR_DIR


def test_package_exposes_version() -> None:
    assert __version__ == "0.1.0"


def test_repo_paths_match_expected_layout() -> None:
    assert SQL_DIR.name == "sql"
    assert VAR_DIR.name == "var"
