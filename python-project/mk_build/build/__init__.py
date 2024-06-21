from collections.abc import Sequence
import os

from mk_build.build.deps import Deps
from mk_build.build.process import run, CompletedProcess
from mk_build.build.path import Path, PathInput, path, path_dir, paths, suffix
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

    return config.get().top_source_dir


def top_build_dir() -> str:
    """ Return the top level build directory. """

    return config.get().top_build_dir


def source_dir() -> Path:
    """ Return a Path to the current source directory. """

    return config.get().source_dir


def source_dir_abs() -> Path:
    """ Return an absolute Path to the current source directory. """

    return path(top_source_dir(), source_dir())


def source_dir_add(paths: Sequence[PathInput]) -> Sequence[Path]:
    """ Concatenate paths to the source directory that corresponds to the
        current build directory. """

    source_dir = config.get().source_dir

    return [path(source_dir, it) for it in paths]


def build_dir() -> Path:
    """ Return a Path to the current build directory. """

    return config.get().build_dir


def build_dir_add(paths: Sequence[PathInput]) -> Sequence[Path]:
    """ Concatenate paths to the current build directory. """

    build_dir = config.get().build_dir

    return [path(build_dir, it) for it in paths]


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
