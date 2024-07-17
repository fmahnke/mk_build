from logging import (debug, info, warning, error, DEBUG, INFO,  # noqa: F401
    WARNING, ERROR, LogRecord)
import logging

from .util import environ

__all__ = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'init']


def set_detail(level: int) -> None:
    if level < 0 or level > len(_detail_str) - 1:
        raise Exception()
    else:
        _formatter.format_str(_detail_str[level])


def set_formatter(formatter: 'Formatter') -> None:
    _handler.setFormatter(formatter)


def set_level(level: int | str) -> None:
    _root_logger.setLevel(level)


# Initialize the global logger

_detail_str = [
    '%(levelname)s: %(message)s',
    '%(levelname)s:%(module)s::%(funcName)s: %(message)s',
    '%(levelname)s:%(name)s:%(module)s::%(funcName)s: %(message)s'
]


_detail_formatter = [
    logging.Formatter(_detail_str[0]),
    logging.Formatter(_detail_str[1]),
    logging.Formatter(_detail_str[2])
]


class Formatter(logging.Formatter):
    grey_0 = "\x1b[38;2;85;85;85m"
    grey_1 = "\x1b[38;2;110;110;110m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self) -> None:
        super().__init__()

        format_str = _detail_str[0]

        self._make_formatters(format_str)

    def format_str(self, format_str: str) -> None:
        self._make_formatters(format_str)

    def format(self, record: LogRecord) -> str:
        if record.levelno >= 50:
            idx = 0
        elif record.levelno >= 40:
            idx = 1
        elif record.levelno >= 30:
            idx = 2
        elif record.levelno >= 20:
            idx = 3
        else:
            idx = 4

        formatter = self._formatters[idx]

        return formatter.format(record)

    def _make_formatters(self, format_str: str) -> None:
        self._formatters = [
            logging.Formatter(self.bold_red + format_str + self.reset),
            logging.Formatter(self.red + format_str + self.reset),
            logging.Formatter(self.yellow + format_str + self.reset),
            logging.Formatter(self.grey_1 + format_str + self.reset),
            logging.Formatter(self.grey_0 + format_str + self.reset)
        ]


_formatter = Formatter()

_handler = logging.StreamHandler()
_root_logger = logging.getLogger('root')
_root_logger.addHandler(_handler)

set_formatter(_formatter)

set_detail(0)


def init(level: str) -> None:
    global _formatter
    global _handler
    global _root_logger

    env_level = environ('MK_LOG_LEVEL', required=False)

    if env_level is None:
        set_level(level)
    else:
        set_level(env_level)


init('WARNING')
