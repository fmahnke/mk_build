from os import chdir

from mk_build.build.path import Path
from mk_build.gup import gup_path
import pytest

from . import test_dir


@pytest.mark.skip(reason="currently unused")
class TestGup:
    def test_gup_path(self) -> None:
        chdir(test_dir)

        assert gup_path('project/gup/subdir_0/subdir_1') == Path('project')
