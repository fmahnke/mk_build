import os
import pathlib
from pathlib import PurePath
import subprocess
import sys

from mk_build.build.deps import Deps
from mk_build.build.path import path, path_dir, paths
import mk_build.config as config
from mk_build.gup import gup


__all__ = ['environ', 'gup', 'path', 'paths', 'deps', 'OK', 'output',
           'path_dir', 'run', 'target', 'source_dir'
           'top_build_dir', 'top_source_dir']

output = sys.argv[1] if len(sys.argv) > 1 else None
target = sys.argv[2] if len(sys.argv) > 2 else None

print(f'output={output}')
print(f'target={target}')


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
    result = pathlib.Path(
        top_source_dir(), result.relative_to(top_build_dir()))

    return result

# def build_dir():
#     cwd = os.getcwd()
#     result = pathlib.PurePath(cwd).relative_to(top_build_dir())
#
#     return result


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


def run(args, **kwargs):
    args = [str(arg) for arg in args]

    print(f"run: {args}")
    print(f"run (dry={config.dry_run}): {' '.join(args)}")

    if config.dry_run:
        code = 0
    else:
        result = subprocess.run(args, **kwargs)
        code = result.returncode

    return code
