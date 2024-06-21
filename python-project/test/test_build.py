import os
import sys

from mk_build import run
from mk_build.build import *
from mk_build.build import build_dir_add, source_dir_add
from mk_build.build.path import *
import mk_build.config as config_


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

        config_.init(build_dir=Path('path'))
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

        config_.init(build_dir=Path('path'))

        top_source_dir_str = '/top/source'
        top_build_dir_str = '/top/source/_build'
        build_dir_str = 'path'
        source_dir_str = build_dir_str

        assert top_source_dir() == Path(top_source_dir_str)

        assert source_dir() == Path(source_dir_str)

        assert source_dir_abs() == Path('/top/source/path')

        assert source_dir_add([]) == []
        assert source_dir_add(['0']) == [Path(f'{source_dir_str}/0')]
        assert source_dir_add(['0', '1']) == [
            Path(f'{source_dir_str}/0'),
            Path(f'{source_dir_str}/1')
        ]

        assert top_build_dir() == Path(top_build_dir_str)

        assert build_dir() == Path(build_dir_str)

        assert build_dir_add([]) == []
        assert build_dir_add(['0']) == [Path(f'{build_dir_str}/0')]
        assert build_dir_add(['0', '1']) == [
            Path(f'{build_dir_str}/0'),
            Path(f'{build_dir_str}/1')
        ]
