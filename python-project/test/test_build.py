from mk_build import config, run


class TestClass:
    def test_run(self):
        config.dry_run = True

        result = run(['true'])

        assert result.returncode == 0
