from inspect import stack
import os.path
import sys
from typing import Any


def todo(message: str) -> None:
    frame = stack()[1]
    file = os.path.basename(frame.filename)
    line = frame.lineno
    print(f'{file}:{line} TODO {message}')


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)
