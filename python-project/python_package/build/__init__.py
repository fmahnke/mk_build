import os
import pathlib
import subprocess

from build.deps import Deps
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

    args = [str(arg) for arg in args]

    print(f"run: {args}")
    print(f"run (dry={config.dry_run}): {' '.join(args)}")

    if config.dry_run:
        code = 0
    else:
        result = subprocess.run(args)
        code = result.returncode

    return code
