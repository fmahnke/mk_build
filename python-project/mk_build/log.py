from logging import (debug, info, warning, error, DEBUG, INFO,  # noqa: F401
    WARNING, ERROR)
import logging

__all__ = ['DEBUG', 'INFO', 'WARNING', 'ERROR']


_handler = logging.StreamHandler()
_root_logger = logging.getLogger('root')
_root_logger.addHandler(_handler)


def set_formatter(formatter) -> None:
    _handler.setFormatter(formatter)


def set_level(level) -> None:
    _root_logger.setLevel(level)
