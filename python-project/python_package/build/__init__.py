import os
import pathlib
import subprocess

import config

def dir(path):
    last_sep = path.rfind('/')
    return path[:last_sep]

def environ(key, allow_empty):
    result = None

    if key in os.environ:
        return os.environ[key]
    elif allow_empty:
        return ''
    else:
        raise Exception()

def top_source_dir():
    return os.environ['srcdir']

def top_build_dir():
    return config.builddir

def source_dir():
    cwd = os.getcwd()
    result = pathlib.Path(cwd)
    result = pathlib.Path(top_source_dir(), result.relative_to(top_build_dir()))

    return result

def run(args):
    args = [str(arg) for arg in args]

    print(f"run: {args}")
    print(f"run (dry={config.dry_run}): {' '.join(args)}")

    if config.dry_run:
        code = 0
    else:
        result = subprocess.run(args)
        code = result.returncode

    return code
