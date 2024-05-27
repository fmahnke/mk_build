import subprocess
from subprocess import CalledProcessError
import os
import sys

import mk_build.config as config
from mk_build.util import eprint


def gup(*targets, env=None, **kwargs):
    args = ["gup", "-u"]

    if config.trace:
        args.append('--trace')

    if isinstance(targets, tuple):
        first = targets[0]

        if isinstance(first, list):
            args += first
        else:
            args += targets
    else:
        args += targets

    args = [str(arg) for arg in args]
    print(f"gup (dry={config.dry_run}): {args}")

    if env is not None:
        print(f'env {env}')
        env = env | os.environ

    if not config.dry_run:
        try:
            result = subprocess.run(args, env=env, check=True, **kwargs)
        except CalledProcessError as e:
            eprint(e)
            # print(f'gup returned {e.returncode}:')
            # print(f'stdout: {e.stdout}')
            # print(f'stderr: {e.stderr}')

            sys.exit(1)

        return result
