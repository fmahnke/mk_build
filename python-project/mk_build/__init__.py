from pathlib import Path

from mk_build.build import *
from mk_build.build import exit
from mk_build.build.target import Target
from mk_build.build.path import Paths, path, paths, suffix
from mk_build.build.process import CalledProcessError
import mk_build.build.tools as tools
from mk_build.gup import bin_o
from mk_build.gup.archive import Archive
from mk_build.gup.assemble import Assemble
from mk_build.gup.cc_and_link import CCompileAndLink
from mk_build.util import eprint
from .build import build_dir_add, source_dir_add

__all__ = [
    'depends',
    'environ',
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
    'Path',
    'Paths',
    # builders
    'bin_o',
    # process
    'CalledProcessError',
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
