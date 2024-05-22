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

print(f'output={output}')
print(f'target={target}')


def dir(path):
    last_sep = path.rfind('/')
    return path[:last_sep]


def environ(key, allow_empty):
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


def source_dir(paths=Optional[list]) -> PurePath | list[PurePath]:
    """ Return the path of the current source directory, relative to the top
        level source directory. """
    cwd = os.getcwd()
    source_dir = PurePath(cwd)
    source_dir = PurePath(
        top_source_dir(), source_dir.relative_to(top_build_dir()))

    if paths is not None:
        return [path(source_dir, it) for it in paths]
    else:
        return source_dir


def build_dir():
    """ Return the path of the current build directory, relative to the top
        level build directory. """
    cwd = os.getcwd()
    result = pathlib.PurePath(cwd).relative_to(top_build_dir())
    return result


def gup_state_path(path):
    return PurePath(*path.parts[:-1], '.gup', *path.parts[-1:])

# def gup_shadow_path(path):
#     return PurePath(*path.parts[:-3], 'gup', *path.parts[-3:])


def deps(path):
    print(f'dpath {path}')
    build_parent = path.parent
    shadow = gup_state_path(path)
    path = PurePath(shadow)
    parent = path.parent

    deps_file = PurePath(parent, f'deps.{path.name}')
    print(f'deps file {deps_file}')
    deps = Deps(deps_file, build_parent)
    print(f'files {deps.files}')
    return deps


def run(args, **kwargs) -> CompletedProcess:
    args = [str(arg) for arg in args]

    print(f"run: {args}")
    print(f"run (dry={config.dry_run}): {' '.join(args)}")

    if config.dry_run:
        result: CompletedProcess = CompletedProcess(args, 0)
    else:
        result = subprocess.run(args, check=True, **kwargs)

    return result
