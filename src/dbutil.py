import os
import pymysql
from parseconf import parse_config, ConfigParserError
from typing import Generator, Tuple
from logging import Logger


class DbConnectionError(Exception):
    pass


class DbExecutionError(Exception):
    pass


def db_connect(
    host: str,
    port: int,
    user: str,
    pwd: str,
    database: str,
    autocommit=True,
    connect_timeout=15,
) -> pymysql.connections.Connection:
    try:
        return pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            database=database,
            charset="utf8",
            autocommit=autocommit,
            connect_timeout=connect_timeout,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as err:
        raise DbConnectionError(err)


class Dbutil:
    def __init__(self, log: Logger) -> None:
        self.log = log
        self.db = self.connect()

    def connect(self):
        if "DB_CONFIG" not in os.environ:
            msg = "Missing DB_CONFIG environment variable."
            self.log.error(msg)
            raise DbConnectionError(msg)

        config_file = os.environ["DB_CONFIG"]

        try:
            user, pwd, host, port, database = parse_config(config_file)
        except ConfigParserError as err:
            msg = f"Failed to parse config file {config_file}: {err}"
            self.log.error(msg)
            raise DbConnectionError(msg)

        self.log.info(
            "Connecting to host=%s, port=%s, database=%s", host, port, database
        )

        try:
            db = db_connect(host=host, port=port, user=user, pwd=pwd, database=database)
        except DbConnectionError as err:
            self.log.error(f"Failed to connect to db: {err}")
            raise

        return db

    def get_sum_users(self, is_subscriber: int = 0) -> int:
        sql = "select count(*) as ct from users where is_subscriber = %s"
        sth = self.db.cursor()

        try:
            sth.execute(sql, [is_subscriber])
            row = sth.fetchone()
        except pymysql.Error as err:
            self.log.error("DB Error: %s", err)
            raise DbExecutionError(err)
        finally:
            sth.close()

        return row["ct"] if row else 0

    def get_email_list(self, is_subscriber: int = 0) -> Generator[Tuple[str, str, str], None, None]:
        #
        # db table: users
        # email, first_name, last_name, is_subscriber
        sql = "select first_name, last_name, email from users where is_subscriber = %s"
        sth = self.db.cursor()

        try:
            sth.execute(sql, [is_subscriber])
        except pymysql.Error as err:
            self.log.error("DB Error: %s", err)
            raise DbExecutionError(err)

        for row in sth.fetchall():
            first_name = row["first_name"]
            last_name = row["last_name"]
            email = row["email"]
            email_expand = f"{first_name} {last_name} <{email}>"  # something like "Jack Wilson <jwilson@xyz.com>"
            yield first_name, last_name, email_expand

        sth.close()
