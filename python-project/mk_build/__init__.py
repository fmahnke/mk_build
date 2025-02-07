from pathlib import Path

from mk_build.build import *
from mk_build.build import exit
from mk_build.build.target import Target
from mk_build.build.path import PathInput, Paths, path, paths, suffix
from mk_build.build.process import CalledProcessError, CompletedProcess
import mk_build.build.tools as tools
from mk_build.gup import bin_o
from mk_build.gup.archive import Archive
from mk_build.gup.assemble import Assemble
from mk_build.gup.cc_and_link import CCompileAndLink
from mk_build.util import environ
from mk_build.util.io import eprint
from .build import build_dir_add, source_dir_add, top_source_dir_add
from .validate import ensure_type

__all__ = [
    'depends',
    'environ',
    'ensure_type',
    'exit',
    'gup',
    'path',
    'path_dir',
    'paths',
    'run',
    # paths
    'build_dir',
    'build_dir_add',
    'source_dir',
    'source_dir_add',
    'source_dir_abs',
    'suffix',
    'top_build_dir',
    'top_source_dir',
    'top_source_dir_add',
    'Path',
    'PathInput',
    'Paths',
    # builders
    'bin_o',
    # process
    'CalledProcessError',
    'CompletedProcess',
    # tools
    'tools',
    # util
    'eprint',
    # targets
    'Archive',
    'Assemble',
    'CCompileAndLink',
    'Target'
]
