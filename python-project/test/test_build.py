import os
import sys

from mk_build import run
from mk_build.build import *
from mk_build.build import build_dir_add, source_dir_add, top_source_dir_add
from mk_build.build.path import *
import mk_build.config as config_
from mk_build.util import chdir

from . import data_dir


class TestClass:
    def test_run(self) -> None:

        config_.get().dry_run = True

        result = run(['true'])

        assert result.returncode == 0


class TestConfig:
    target = Path('path/file.suffix')

    sys.argv = [
        'gup',
        '/top/source/_build/path/.gup/out.file.suffix',
        str(target)
    ]

    top_source_dir = Path(data_dir)
    top_build_dir = Path(data_dir, '_build')

    subdir_0 = Path(top_build_dir, 'subdir_0')

    config = config_.get()

    def setup_method(self) -> None:
        os.makedirs(self.subdir_0, exist_ok=True)

        os.environ['top_source_dir'] = str(self.top_source_dir)
        os.environ['top_build_dir'] = str(self.top_build_dir)

        chdir(self.config.top_build_dir)

    def test_dirs(self) -> None:
        _source_dir = Path(self.target.parent)
        _build_dir = Path(self.target.parent)

        config = self.config

        # indirect target

        chdir(config.top_build_dir)

        assert config.top_source_dir == self.top_source_dir
        assert config.top_build_dir == self.top_build_dir
        assert config.source_dir == _source_dir
        assert config.build_dir == _build_dir

        from mk_build.build import build_dir

        assert source_dir() == _source_dir
        assert build_dir() == _build_dir

        assert source_dir_abs() == Path(self.top_source_dir, _source_dir)

        # direct target

        chdir(Path(self.top_build_dir, 'subdir_0'))

        _source_dir = Path('subdir_0')
        _build_dir = Path('subdir_0')

        assert source_dir() == _source_dir
        assert build_dir() == _build_dir

        assert source_dir_abs() == Path(self.top_source_dir, _source_dir)

    def test_path(self) -> None:
        build_dir_str = 'path'
        source_dir_str = build_dir_str

        assert top_source_dir() == self.top_source_dir
        assert top_source_dir_add('0') == [Path(self.top_source_dir, '0')]

        assert source_dir_add([]) == []
        assert source_dir_add(['0']) == [Path(f'{source_dir_str}/0')]
        assert source_dir_add(['0', '1']) == [
            Path(f'{source_dir_str}/0'),
            Path(f'{source_dir_str}/1')
        ]

        assert top_build_dir() == Path(self.top_build_dir)

        assert build_dir_add([]) == []
        assert build_dir_add(['0']) == [Path(f'{build_dir_str}/0')]
        assert build_dir_add(['0', '1']) == [
            Path(f'{build_dir_str}/0'),
            Path(f'{build_dir_str}/1')
        ]
