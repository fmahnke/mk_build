from collections.abc import Sequence

from mk_build.build.deps import Deps
from mk_build.build.process import run, CompletedProcess
from mk_build.build.path import Path, PathInput, path, path_dir, paths, suffix
import mk_build.config as config
from mk_build.gup import gup
import mk_build.log as log
from ..validate import ensure_type


__all__ = [
    'build_dir',
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


def dir(path: str) -> str:
    """ Return the directory part of path. """

    last_sep = path.rfind('/')
    return path[:last_sep]


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

    return str(config.get().top_source_dir)


def top_source_dir_add(paths: Sequence[PathInput]) -> Sequence[Path]:
    """ Concatenate paths to the topsource directory. """

    top_source_dir = ensure_type(config.get().top_source_dir, Path)

    return [path(top_source_dir, it) for it in paths]


def top_build_dir() -> str:
    """ Return the top level build directory. """

    return ensure_type(config.get().top_build_dir, str)


def source_dir() -> Path:
    """ Return a Path to the current source directory. """

    return ensure_type(config.get().source_dir, Path)


def source_dir_abs() -> Path:
    """ Return an absolute Path to the current source directory. """

    return path(top_source_dir(), source_dir())


def source_dir_add(paths: Sequence[PathInput]) -> Sequence[Path]:
    """ Concatenate paths to the source directory that corresponds to the
        current build directory. """

    source_dir = ensure_type(config.get().source_dir, Path)

    return [path(source_dir, it) for it in paths]


def build_dir() -> Path:
    """ Return a Path to the current build directory. """

    return ensure_type(config.get().build_dir, Path)


def build_dir_add(paths: Sequence[PathInput]) -> Sequence[Path]:
    """ Concatenate paths to the current build directory. """

    build_dir = ensure_type(config.get().build_dir, Path)

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
