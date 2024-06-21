import os
import sys

from mk_build import run
from mk_build.build import *
from mk_build.build.path import *
import mk_build.config as config_
from mk_build.config import Config


class TestClass:
    def test_run(self) -> None:

        config_.get().dry_run = True

        result = run(['true'])

        assert result.returncode == 0


class TestConfig:
    def test_dirs(self) -> None:
        sys.argv = [
            'gup',
            '/top/source/_build/path/.gup/out.file.suffix',
            'path/file.suffix'
        ]

        os.environ['top_source_dir'] = '/top/source'
        os.environ['top_build_dir'] = '/top/source/_build'

        config_.init()

        config = config_.get()

        assert config.build_dir == Path('path')
        assert config.source_dir == Path('path')

        from mk_build.build import build_dir

        assert build_dir() == Path('path')


class TestPath:
    def test_path(self) -> None:
        sys.argv = [
            'gup',
            '/top/source/_build/path/.gup/out.file.suffix',
            'path/file.suffix'
        ]

        os.environ['top_source_dir'] = '/top/source'
        os.environ['top_build_dir'] = '/top/source/_build'

        config = Config()

        print(f'topsrc {config.top_source_dir}')
        print(f'src {config.source_dir}')

        assert source_dir_abs() == Path('/top/source/path')

        assert (Path(source_dir_abs(), "include")
                == Path('/top/source/path/include'))
