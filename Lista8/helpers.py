import logging
import sys
from datetime import datetime

import pytz


def safe_int(value):
    try:
        return int(value)
    except ValueError:
        return 0

def parse_timestamp(timestamp_str):
    timestamp_str = timestamp_str.strip('[]')
    try:
        return datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        return datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S").replace(tzinfo=pytz.UTC)


def get_logger(name="logger", enabled=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger