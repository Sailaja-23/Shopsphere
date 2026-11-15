import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "shopsphere.log"

    log_format = (
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    formatter = logging.Formatter(log_format)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    else:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
