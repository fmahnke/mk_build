import os
import sys
from typing import Optional

import mk_build.config as config
import mk_build.build.process as process
from mk_build.build.process import CalledProcessError, CompletedProcess
from mk_build.util import eprint


def gup(*targets, **kwargs) -> Optional[CompletedProcess]:
    """ Execute gup for targets. """

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
        result = None
    else:
        try:
            result = process.run(args, **kwargs)
        except CalledProcessError as e:
            eprint(e)
            # print(f'gup returned {e.returncode}:')
            # print(f'stdout: {e.stdout}')
            # print(f'stderr: {e.stderr}')

            sys.exit(1)

    return result
