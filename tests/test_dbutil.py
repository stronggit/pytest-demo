import os
import sys
import pytest
from pathlib import Path

pardir = Path(__file__).parent.parent.as_posix()
sys.path.append(os.path.join(pardir, "src"))
from src.dbutil import Dbutil, DbConnectionError, DbExecutionError  # noqa E402
from src.log import setup_logger  # noqa E402


def test_good_connection(mock_mysql, mock_config_file):

    log = setup_logger("test")
    os.environ["DB_CONFIG"] = mock_config_file

    try:
        Dbutil(log=log)
    except Exception:
        assert False
    else:
        assert True


def test_bad_connection(mock_mysql, mock_config_file):

    log = setup_logger("test")
    os.environ["DB_CONFIG"] = mock_config_file

    # test bad connection exception
    mock_mysql.raiseConnectionError = True

    with pytest.raises(DbConnectionError):
        Dbutil(log=log)

    # test bad config file exception
    os.environ.pop("DB_CONFIG")

    mock_mysql.raiseConnectionError = False

    with pytest.raises(DbConnectionError):
        Dbutil(log=log)


def test_bad_config(mock_mysql, mock_bad_config_file):

    log = setup_logger("test")

    os.environ["DB_CONFIG"] = mock_bad_config_file

    with pytest.raises(DbConnectionError):
        Dbutil(log=log)


def test_get_sum_users(mock_mysql, mock_config_file):

    log = setup_logger("test")
    os.environ["DB_CONFIG"] = mock_config_file

    mock_mysql.result = [{"ct": 10}]

    db = Dbutil(log=log)
    count = db.get_sum_users()
    assert count == 10

    mock_mysql.raiseExecutionError = True

    with pytest.raises(DbExecutionError):
        db.get_sum_users()


def test_get_email_list(mock_mysql, mock_config_file):

    log = setup_logger("test")
    os.environ["DB_CONFIG"] = mock_config_file

    exp_vals = [
        {"first_name": "John", "last_name": "Doe", "email": "johndoe@abc.com"},
        {"first_name": "Jane", "last_name": "Doe", "email": "janedoe@xyz.com"},
    ]
    mock_mysql.result = exp_vals
    db = Dbutil(log=log)

    for idx, row in enumerate(db.get_email_list()):
        exp_first_name = exp_vals[idx]["first_name"]
        exp_last_name = exp_vals[idx]["last_name"]
        exp_email = exp_vals[idx]["email"]
        assert row[0] == exp_first_name
        assert row[1] == exp_last_name
        assert row[2] == f"{exp_first_name} {exp_last_name} <{exp_email}>"

    mock_mysql.raiseExecutionError = True
    with pytest.raises(DbExecutionError):
        for _ in db.get_email_list():
            pass
