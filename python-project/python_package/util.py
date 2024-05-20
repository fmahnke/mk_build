from inspect import getframeinfo, stack
import os.path

def todo(message):
    frame = stack()[1]
    file = os.path.basename(frame.filename)
    line = frame.lineno
    print(f'{file}:{line} TODO {message}')
