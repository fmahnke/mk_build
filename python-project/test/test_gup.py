from os import chdir

from mk_build.build.path import Path
from mk_build.gup import gup_path

from . import test_dir


class TestGup:
    def test_gup_path(self):
        chdir(test_dir)

        assert gup_path('project/gup/subdir_0/subdir_1') == Path('project')
