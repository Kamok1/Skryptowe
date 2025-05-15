import logging
import os
import sys
from logging import Logger
from typing import Optional


def _parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "t"}

def get_logger(name: str = "logger", enabled: Optional[bool] = None) -> Logger:
    logger = logging.getLogger(name)
    if enabled is None:
        enabled = _parse_bool(os.getenv("LOG_ENABLED", "0"))

    if not enabled:
        logger.disabled = True
        return logger

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