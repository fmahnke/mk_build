import os
import pathlib
from pathlib import PurePath
import subprocess
from subprocess import CompletedProcess
import sys
from typing import Optional

from mk_build.build.deps import Deps
from mk_build.build.path import path, path_dir, paths, suffix
import mk_build.config as config
from mk_build.gup import gup
import mk_build.log as log


__all__ = [
    'build_dir',
    'environ',
    'gup',
    'path',
    'paths',
    'deps',
    'output',
    'path_dir',
    'run',
    'target',
    'source_dir',
    'suffix',
    'top_build_dir',
    'top_source_dir'
]

output = sys.argv[1] if len(sys.argv) > 1 else None
target = sys.argv[2] if len(sys.argv) > 2 else None

log.debug(f'output={output}')
log.debug(f'target={target}')


def dir(path):
    """ Return the directory part of path. """

    last_sep = path.rfind('/')
    return path[:last_sep]


def environ(key, allow_empty):
    """ Return the value of an environment variable.

    If key names a variable in the environment, return its value. If the named
    variable does not exist and allow_empty == True, return ''. Otherwise,
    raise an exception.
    """

    if key in os.environ:
        return os.environ[key]
    elif allow_empty:
        return ''
    else:
        raise Exception()


def top_source_dir():
    """ Return the top level source directory.

    The top level source directory is the value of the environment variable
    'srcdir'.
    """

    return os.environ['srcdir']


def top_build_dir():
    """ Return the top level build directory. """

    return config.builddir


def source_dir(paths=Optional[list]) -> PurePath | list[PurePath]:
    """ Concatenate zero or more paths to the source directory that
        corresponds to the current build directory. """

    cwd = os.getcwd()
    source_dir = PurePath(cwd)
    source_dir = PurePath(
        top_source_dir(), source_dir.relative_to(top_build_dir()))

    if paths is not None:
        return [path(source_dir, it) for it in paths]
    else:
        return source_dir


def build_dir(paths=Optional[list]) -> PurePath | list[PurePath]:
    """ Concatenate zero or more paths to the current build directory. """

    cwd = os.getcwd()
    build_dir = pathlib.PurePath(cwd).relative_to(top_build_dir())

    if paths is not None:
        return [path(build_dir, it) for it in paths]
    else:
        return build_dir


def gup_state_path(path):
    return PurePath(*path.parts[:-1], '.gup', *path.parts[-1:])

# def gup_shadow_path(path):
#     return PurePath(*path.parts[:-3], 'gup', *path.parts[-3:])


def deps(path):
    log.debug(f'dpath {path}')
    build_parent = path.parent
    shadow = gup_state_path(path)
    path = PurePath(shadow)
    parent = path.parent

    deps_file = PurePath(parent, f'deps.{path.name}')
    log.debug(f'deps file {deps_file}')
    deps = Deps(deps_file, build_parent)
    log.debug(f'files {deps.files}')
    return deps


def run(args, **kwargs) -> CompletedProcess:
    """ Execute a program in a child process. """

    args = [str(arg) for arg in args]

    if config.dry_run:
        dry = ' (dry run)'
    else:
        dry = ''

    log.info(f"run: {' '.join(args)}{dry}")

    if config.dry_run:
        result: CompletedProcess = CompletedProcess(args, 0)
    else:
        result = subprocess.run(args, check=True, **kwargs)

    return result
