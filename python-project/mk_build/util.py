from inspect import stack
import os.path
import sys


def todo(message):
    frame = stack()[1]
    file = os.path.basename(frame.filename)
    line = frame.lineno
    print(f'{file}:{line} TODO {message}')


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
