from pathlib import PurePath

from mk_build.gup import gup_path


class TestGup:
    def test_gup_path(self):
        assert (gup_path('test/project/gup/subdir_0/subdir_1')
            == PurePath('test/project'))
