#!/usr/bin/env python

import os
from logging import Logger
from pathlib import Path
from dbutil import Dbutil
from log import setup_logger
from typing import Union


def sendmail(log: Logger, email: str, body: str, attachment: Union[str, None] = None) -> None:
    if attachment:
        log.info(f"Sending email to {email} with attachment {attachment}")
        log.info(f"  -- {body}")
    else:
        log.info(f"Sending email to {email}")
        log.info(f"  -- {body}")


def create_logger():
    pardir = Path(__file__).resolve().parent.parent.as_posix()
    log_file = os.path.join(pardir, "log", "main.log")  # ../log/main.log
    return setup_logger("pytest_demo", log_file=log_file)


def main():
    log = create_logger()
    db = Dbutil(log=log)

    # Get list of subscribers and send discount offer
    if db.get_sum_users(is_subscriber=1):
        for first_name, _, email in db.get_email_list(is_subscriber=1):
            body = f"Welcome {first_name}, please enjoy this week's newsletter and our special discount offer."
            attachment = "discount_offer.pdf"
            sendmail(log, email, body, attachment)

    if db.get_sum_users(is_subscriber=0):
        for first_name, _, email in db.get_email_list(is_subscriber=0):
            body = f"Welcome {first_name}, please enjoy this week's newsletter."
            sendmail(log, email, body)


if __name__ == "__main__":
    main()
