from logging import (debug, info, warning, error, DEBUG, INFO,  # noqa: F401
    WARNING, ERROR)
import logging

__all__ = ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def set_detail(level: int) -> None:
    if level < 0 or level > len(_detail_formatter) - 1:
        raise Exception()
    else:
        set_formatter(_detail_formatter[level])


def set_formatter(formatter) -> None:
    _handler.setFormatter(formatter)


def set_level(level) -> None:
    _root_logger.setLevel(level)


# Initialize the global logger

_detail_str = [
    '%(levelname)s:%(message)s',
    '%(levelname)s:%(module)s::%(funcName)s:%(message)s',
    '%(levelname)s:%(name)s:%(module)s::%(funcName)s:%(message)s'
]

_detail_formatter = [
    logging.Formatter(_detail_str[0]),
    logging.Formatter(_detail_str[1]),
    logging.Formatter(_detail_str[2])
]

_handler = logging.StreamHandler()
_root_logger = logging.getLogger('root')
_root_logger.addHandler(_handler)

set_detail(0)
