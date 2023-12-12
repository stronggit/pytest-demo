import sys
import os
import pymysql
import pytest
from pathlib import Path


@pytest.fixture()
def mock_mysql(monkeypatch):
    class MockConnection:
        def __init__(self):
            if data.raiseConnectionError:
                raise pymysql.Error

        @staticmethod
        def cursor(*arg, **kwargs):
            return Cursor()

    class Cursor:
        @staticmethod
        def execute(*args, **kwargs):
            if data.raiseExecutionError:
                raise pymysql.Error

        @staticmethod
        def fetchone(*args, **kwargs):
            if data.result:
                return data.result[0]

        @staticmethod
        def fetchall(*args, **kwargs):
            if data.result:
                for row in data.result:
                    yield row

        @staticmethod
        def close():
            pass

    def mock_connection(*args, **kwargs):
        return MockConnection()

    monkeypatch.setattr(pymysql, "connect", mock_connection)

    class Data:
        def __init__(self):
            self.result = []
            self.raiseConnectionError = False
            self.raiseExecutionError = False

    data = Data()
    return data


@pytest.fixture()
def mock_config_file(tmp_path):
    """Fixture to create a mockup db config file."""

    body = """
[database]
user = test
password = pwd123
host = localhost
port = 3306
database = testdb
""".strip()

    fileobj = tmp_path / "db.config"
    fileobj.write_text(body)
    return fileobj.as_posix()


@pytest.fixture()
def mock_bad_config_file(tmp_path):
    """Fixture to create a mockup db config file."""

    body = """
[database]
host = localhost
port = 3306
database = testdb
""".strip()

    fileobj = tmp_path / "db.config"
    fileobj.write_text(body)
    return fileobj.as_posix()
