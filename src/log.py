import sys
import logging
from logging import Logger, handlers
from typing import Union


def setup_logger(
    name: str,
    log_file: Union[str, None] = None,
    log_level: str = "INFO",
    stdout: bool = True,
    max_bytes: int = 100_000_000,
    backup_count: int = 3,
    format: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
) -> Logger:
    """Configure logging for the package.
    """
    valid_log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    if log_level not in valid_log_levels:
        raise ValueError(
            f"Invalid log level: {log_level}; valid levels are {valid_log_levels}"
        )

    formatter = logging.Formatter(
        fmt=format
    )

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not log_file or stdout:
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.setFormatter(formatter)
        logger.addHandler(handler_stdout)

    if log_file is not None:
        # Rotational log: 100MB each, total 4 log files
        handler_file = handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        handler_file.setFormatter(formatter)
        logger.addHandler(handler_file)

    return logger
