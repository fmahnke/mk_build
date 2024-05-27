import subprocess
from subprocess import CalledProcessError
import os
import sys

import mk_build.config as config
import mk_build.log as log
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

    if config.dry_run:
        dry = ' (dry run)'
    else:
        dry = ''

    log.info(f"{' '.join(args)}{dry}")

    if env is not None:
        for k, v in env.items():
            log.info(f'    {k} = {v}')
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
