"""Centralised logging configuration for the application."""

import logging
import sys


def setup_logging() -> logging.Logger:
    """Configure the root logger and return the application-level logger.

    Sets up a single :class:`logging.StreamHandler` writing to *stdout* with a
    consistent timestamp + level + name format.  Third-party loggers that
    produce excessive output are silenced to WARNING level.

    Returns:
        A :class:`logging.Logger` instance named ``"readme_generator"``.
    """
    fmt = "%(asctime)s | %(levelname)-8s | %(name)-22s | %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"))

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:
        root.addHandler(handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging.getLogger("readme_generator")


logger = setup_logging()
