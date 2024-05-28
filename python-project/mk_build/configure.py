""" This module creates a build configuration file. """

import os
import sys

from mk_build.config import Config
from mk_build.gup import gup_path
import mk_build.log as log


def main() -> int:
    """ Create a build configuration file. """

    if 'source_dir' in os.environ:
        source_dir = os.environ['source_dir']
    else:
        source_dir = str(gup_path(os.getcwd()))
        log.info(f'Auto-detected source directory: {source_dir}')

    if 'build_dir' in os.environ:
        build_dir = os.environ['build_dir']
    else:
        build_dir = os.getcwd()
        log.info(f'Auto-detected build directory: {build_dir}')

    config_file = Config()
    config_file.init(source_dir, build_dir)
    config_file.write('config.toml')

    return 0


if __name__ == '__main__':
    sys.exit(main())
