import os
from os.path import exists
import sys
from typing import Optional

import tomlkit as toml
from tomlkit import TOMLDocument
from tomlkit.items import Table

from . import log
from .build.path import Path
from .util import cwd, environ
from .message import build_dir_error
from .validate import ensure_type


class BaseConfig:
    """ Build configuration file. """

    @classmethod
    def from_file(cls, path: str) -> 'BaseConfig':
        """ Parse the configuration from an existing file. """

        ctx = cls()
        ctx._init_from_file(path)

        return ctx

    def toml(self) -> TOMLDocument:
        return self.config

    def write(self, path: str, mode='w') -> None:
        """ Write the configuration to a file. """

        config_toml = self.toml()

        with open(path, mode) as fi:
            if mode == 'a':
                fi.write('\n')

            fi.write(toml.dumps(config_toml))

    def _init_from_file(self, path: str) -> None:
        with open(path, 'r') as fi:
            self.config = toml.parse(fi.read())

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value


class Config(BaseConfig):
    def __init__(
        self,
        top_source_dir: Optional[Path] = None,
        top_build_dir: Optional[Path] = None,
        log_level: str = 'WARNING',
        verbose: int = 0,
        dry_run: Optional[bool] = None,
        *args,
        **kwargs
    ) -> None:
        """ Initialize the configuration file with arguments. """

        super().__init__(*args, **kwargs)

        self._top_source_dir = None
        self._top_build_dir = None

        self.log_level = log_level
        self.verbose = verbose
        self.dry_run = dry_run

        self.top_source_dir = top_source_dir
        self.top_build_dir = top_build_dir

        '''
        if 'build_source_dir' in os.environ:
            build_source_dir: Optional[str] = os.environ['build_source_dir']
        elif top_source_dir is not None:
            build_source_dir = str(top_source_dir)
        else:
            build_source_dir = None

        if build_source_dir is not None:
            gup_path = f'{build_source_dir}/gup'

            if gup_path not in sys.path:
                sys.path.append(gup_path)

        print(sys.path)
        '''

    @property
    def output(self) -> Optional[Path]:
        return Path(sys.argv[1]) if len(sys.argv) > 1 else None

    @property
    def target(self) -> Optional[Path]:
        return Path(sys.argv[2]) if len(sys.argv) > 2 else None

    @property
    def top_source_dir(self) -> Optional[Path]:
        if self._top_source_dir is not None:
            return self._top_source_dir
        elif 'top_source_dir' not in os.environ:
            return None
        else:
            return Path(environ('top_source_dir', required=True))

    @top_source_dir.setter
    def top_source_dir(self, val: Optional[Path]) -> None:
        if val is None:
            result = None
        else:
            result = Path(val)

        self._top_source_dir = result

    @property
    def top_build_dir(self) -> Optional[Path]:
        if self._top_build_dir is not None:
            return self._top_build_dir
        elif 'top_build_dir' not in os.environ:
            return None
        else:
            return Path(environ('top_build_dir', required=True))

    @top_build_dir.setter
    def top_build_dir(self, val: Optional[Path]) -> None:
        if val is None:
            result = None
        else:
            result = Path(val)

        self._top_build_dir = result

    @property
    def source_dir(self) -> Optional[Path]:
        build_dir = self.build_dir

        if self.top_source_dir is None or build_dir is None:
            return None
        elif self.top_source_dir.is_relative_to(build_dir):
            return self.top_source_dir.relative_to(build_dir)
        else:
            return build_dir

    @property
    def build_dir(self) -> Optional[Path]:
        build_dir = None

        if cwd() == self.top_build_dir:
            # indirect gup target (builder found through Gupfile)

            if self.target is None:
                build_dir = None
            else:
                build_dir = self.target.parent
        else:
            # direct target

            if self.top_build_dir is not None:
                if Path(self.top_build_dir).is_relative_to(os.getcwd()):
                    build_dir = Path(self.top_build_dir).relative_to(
                        os.getcwd())
                elif Path(os.getcwd()).is_relative_to(self.top_build_dir):
                    build_dir = Path(os.getcwd()).relative_to(
                        self.top_build_dir)
                else:
                    raise AssertionError(str.format(
                        build_dir_error, os.getcwd(), self.top_build_dir
                    ))

        return build_dir

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """ Parse the configuration from an existing file. """

        with open(path, 'r') as fi:
            config = toml.parse(fi.read())

        if not isinstance(config['build'], Table):
            raise Exception('Table is expected.')
        else:
            build = config['build']

            top_source_dir = build.get('source_dir')
            top_build_dir = build.get('build_dir')

            if ensure_type(top_source_dir, str):
                top_source_dir = Path(top_source_dir)
            else:
                top_source_dir = None

            if ensure_type(top_build_dir, str):
                top_build_dir = Path(top_build_dir)
            else:
                top_build_dir = None

            ctx: 'Config' = Config(
                top_source_dir,
                top_build_dir,
                log_level=build.get('log_level') or 'WARNING',
                verbose=build.get('verbose') or 0
            )

        return ctx

    def write(self, path: str, mode=None) -> None:
        """ Write the configuration to a file. """

        self.config = toml.document()

        build = toml.table()

        if self.top_source_dir is not None:
            build.add('source_dir', str(self.top_source_dir))
        if self.top_build_dir is not None:
            build.add('build_dir', str(self.top_build_dir))
        if self.dry_run is not None:
            build.add('dry_run', self.dry_run)

        build.add('log_level', self.log_level)
        build.add('verbose', self.verbose)

        self.config.add('build', build)

        if mode is None:
            mode = 'w'

        super().write(path, mode)

    def __str__(self) -> str:
        return (f'Config(top_source_dir={self.top_source_dir}'
            f', top_build_dir={self.top_build_dir}'
            f', source_dir={self.source_dir}'
            f', build_dir={self.build_dir})')


def _set_top_build_dir() -> Path:
    # If this is the primary build runner, we don't know the top build
    # directory yet. Prioritize setting it via environment variable. Otherwise,
    # gup will have set the working directory to that of the target, so use
    # that.

    if 'top_build_dir' in os.environ:
        top_build_dir = os.environ['top_build_dir']

        log.info(f'top_build_directory from environment: {top_build_dir}')
    else:
        top_build_dir = os.getcwd()
        os.environ['top_build_dir'] = top_build_dir

        log.info(f'Auto-detected build directory: {top_build_dir}')

    return Path(top_build_dir)


def _create(*args, **kwargs) -> Config:
    top_build_dir = _set_top_build_dir()

    config_path = f'{top_build_dir}/config.toml'

    if exists(config_path):
        config = Config.from_file(config_path)

        log.set_level(config.log_level)
    else:
        config = Config(*args, **kwargs)

    return config


config = _create()


def get():
    return config
