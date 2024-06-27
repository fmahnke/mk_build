import os.path
import platform
from typing import Optional

from ..build.path import Path, PathInput


def cwd() -> Path:
    return Path(os.getcwd())


def chdir(path: PathInput) -> None:
    os.chdir(str(path))


def isdir(path: Optional[PathInput]) -> bool:
    if path is None:
        return False
    else:
        return os.path.isdir(path)


def environ(key, default=None, required=True) -> str:
    """ Return the value of an environment variable.

    If key names a variable in the environment, return its value. If the
    variable isn't set and default is not None, return default. If default is
    None, then None is returned if required is False, and an Exception is
    raised if required is True.
    """

    if key in os.environ:
        return os.environ[key]
    elif default is None and required:
        raise Exception(
            f'{key} is a required environment variable, but is not set.'
        )
    else:
        return default


def system():
    # TODO may not actually need this

    if os.path.isfile('/proc/sys/fs/binfmt_misc/WSLInterop'):
        return 'wsl'
    else:
        return platform.system()
