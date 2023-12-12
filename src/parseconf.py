import os
import configparser
from typing import Tuple


class ConfigParserError(Exception):
    pass


def parse_config(config_file) -> Tuple[str, str, str, int, str]:
    # config_file = os.environ.get("DB_CONFIG")

    # if not config_file or not os.path.isfile(config_file):
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file {config_file} not found")

    parser = configparser.ConfigParser()
    parser.read(config_file)

    section = "database"
    if parser.has_option(section, "user"):
        user = parser.get(section, "user")
    else:
        raise ConfigParserError("Missing user in config file")

    if parser.has_option(section, "password"):
        pwd = parser.get(section, "password")
    else:
        raise ConfigParserError("Missing password in config file")

    if parser.has_option(section, "host"):
        host = parser.get(section, "host")
    else:
        raise ConfigParserError("Missing host in config file")

    if parser.has_option(section, "port"):
        port = int(parser.get(section, "port"))
    else:
        raise ConfigParserError("Missing port in config file")

    if parser.has_option(section, "database"):
        database = parser.get(section, "database")
    else:
        raise ConfigParserError("Missing database in config file")

    return user, pwd, host, port, database
