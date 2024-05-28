import os
from os.path import exists

import tomlkit as toml

import mk_build.log as log
from mk_build.log import *


class Config:
    """ Build configuration file. """

    def __init__(self) -> None:
        self.config = toml.document()

    def init(self, source_dir: str, build_dir: str) -> None:
        """ Initialize the configuration file with arguments. """

        self.config = toml.document()
        build = toml.table()
        build.add('source_dir', source_dir)
        build.add('build_dir', build_dir)

        self.config.add('build', build)

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """ Parse the configuration from an existing file. """

        with open(path, 'r') as fi:
            ctx = cls()
            ctx.config = toml.parse(fi.read())
            return ctx

    def write(self, path: str) -> None:
        """ Write the configuration to a file. """

        with open(path, 'w') as fi:
            fi.write(toml.dumps(self.config))


dry_run = False
trace = False

log.set_level(INFO)

if 'top_build_dir' in os.environ:
    top_build_dir = os.environ['top_build_dir']
else:
    top_build_dir = os.getcwd()

build_dir = os.getcwd()

log.debug(f'top_build_dir={top_build_dir}')
log.debug(f'build_dir={build_dir}')

_config_path = f'{top_build_dir}/config.toml'

if exists(_config_path):
    config = Config.from_file(_config_path)
else:
    config = Config()
