import os
import pathlib
from pathlib import Path
from typing import Optional

from mk_build.build.deps import Deps
from mk_build.build.process import run, CompletedProcess
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
    'depends',
    'path_dir',
    'run',
    'source_dir',
    'source_dir_abs',
    'suffix',
    'top_build_dir',
    'top_source_dir'
]


def dir(path):
    """ Return the directory part of path. """

    last_sep = path.rfind('/')
    return path[:last_sep]


def environ(key, allow_empty) -> str:
    """ Return the value of an environment variable.

    If key names a variable in the environment, return its value. If the named
    variable does not exist and allow_empty == True, return ''. Otherwise,
    raise an exception.
    """

    # TODO instead of returning empty value, allow a default value.

    if key in os.environ:
        return os.environ[key]
    elif allow_empty:
        return ''
    else:
        raise Exception()


def exit(result: CompletedProcess | int) -> int:
    if isinstance(result, CompletedProcess):
        return result.returncode
    else:
        return result


def top_source_dir() -> str:
    """ Return the top level source directory.

    The top level source directory is the value of the environment variable
    'srcdir'.
    """

    return os.environ['srcdir']


def top_build_dir() -> str:
    """ Return the top level build directory. """

    return config.top_build_dir


def source_dir(paths: Optional[list] = None) -> Path | list[Path]:
    """ Concatenate zero or more paths to the source directory that
        corresponds to the current build directory. """

    # top_build_dir = '/top_source_dir/_build'
    # build_dir = '_build/target'
    # result = '/top_source_dir/_build/target'

    build_dir_ = build_dir()

    assert isinstance(build_dir_, Path)

    relative_build_dir = Path(*build_dir_.parts[1:])

    source_dir = Path(top_source_dir(), relative_build_dir)

    if paths is not None:
        return [path(source_dir, it) for it in paths]
    else:
        return source_dir


def source_dir_abs(paths: Optional[list] = None) -> Path | list[Path]:
    if paths is not None:
        return [path(top_source_dir(), source_dir(), it) for it in paths]
    else:
        return path(top_source_dir(), source_dir())


def build_dir(paths: Optional[list] = None) -> Path | list[Path]:
    """ Concatenate zero or more paths to the current build directory. """

    # The gup target argument doesn't reliably show the directory containing
    # the target. The gup output argument does, in the format
    # /absolute/path/to/target/.gup/out.<targetname>

    if config.get().output is None:
        raise Exception('gup output path is not available')

    build_dir_parts = pathlib.Path(config.get().output).parts
    gup = build_dir_parts.index('.gup')
    build_dir = pathlib.Path(*build_dir_parts[0:gup])
    build_dir = Path(Path(config.top_build_dir).name,
        build_dir.relative_to(config.top_build_dir))

    if paths is not None:
        return [path(build_dir, it) for it in paths]
    else:
        return build_dir


def gup_state_path(path: Path) -> Path:
    return Path(*path.parts[:-1], '.gup', *path.parts[-1:])

# def gup_shadow_path(path):
#     return Path(*path.parts[:-3], 'gup', *path.parts[-3:])


def depends(path: Path) -> Deps:
    log.debug(f'dpath {path}')
    build_parent = path.parent
    shadow = gup_state_path(path)
    path = Path(shadow)
    parent = path.parent

    deps_file = Path(parent, f'deps.{path.name}')
    log.debug(f'deps file {deps_file}')
    deps = Deps(deps_file, build_parent)
    log.debug(f'files {deps.files}')
    return deps
