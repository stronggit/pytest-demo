import os
import sys
import pytest
from pathlib import Path

pardir = Path(__file__).parent.parent.as_posix()
sys.path.append(os.path.join(pardir, "src"))
from src.parseconf import parse_config, ConfigParserError  # noqa E402


db_config_good = """
[database]
user = test
password = pwd123
host = localhost
port = 3306
database = testdb
""".strip()

db_config_missing_user = """
[database]
password = pwd123
host = localhost
port = 3306
database = testdb
""".strip()

db_config_missing_password = """
[database]
user = test
host = localhost
port = 3306
database = testdb
""".strip()

db_config_missing_host = """
[database]
user = test
password = pwd123
port = 3306
database = testdb
""".strip()

db_config_missing_port = """
[database]
user = test
password = pwd123
host = localhost
database = testdb
""".strip()

db_config_missing_database = """
[database]
user = test
password = pwd123
host = localhost
port = 3306
""".strip()


def create_file(tmp_path, body):
    f = tmp_path / "db.config"
    f.write_text(body)
    return f.as_posix()


def test_parse_missing_config_file():
    with pytest.raises(FileNotFoundError):
        _, _, _, _, _ = parse_config("/no/file/db.config")


@pytest.mark.parametrize(
    "db_config_entry, is_test_good",
    [
        (db_config_good, True),
        (db_config_missing_user, False),
        (db_config_missing_password, False),
        (db_config_missing_host, False),
        (db_config_missing_port, False),
        (db_config_missing_database, False),
    ]
)
def test_parse_config_bad(db_config_entry, is_test_good, tmp_path):
    mock_config_file = create_file(tmp_path, db_config_entry)

    if is_test_good:
        user, pwd, host, port, database = parse_config(mock_config_file)
        assert user == "test"
        assert pwd == "pwd123"
        assert host == "localhost"
        assert port == 3306
        assert database == "testdb"

    else:
        with pytest.raises(ConfigParserError):
            _, _, _, _, _ = parse_config(mock_config_file)
