from pathlib import Path
import os
import sys
from typing import Optional

import mk_build.build.process as process
from mk_build.build.process import CalledProcessError, CompletedProcess
import mk_build.config
from mk_build.config import config
from mk_build.util import eprint


def gup_path(path) -> Optional[Path]:
    """ Return the first parent directory of path that contains a directory
        called \"gup\", or None if it doesn't exist. """

    path_ = path
    it = None

    while True:
        path__ = Path(path_)

        files = os.listdir(path__)

        if 'gup' in files:
            it = path__

        if len(path__.parents) == 0:
            break

        path_ = path__.parents[0]

    return it


def gup(*targets, env=None, **kwargs) -> Optional[CompletedProcess]:
    """ Execute gup for targets. """

    args = ["gup", "-u"]

    if config.verbose == 0:
        args.append('-q')

    if config.verbose > 0:
        args.append('--trace')

    if config.verbose > 1:
        args.append('--verbose')

    target_list = []

    if isinstance(targets, tuple):
        first = targets[0]

        if isinstance(first, list):
            target_list += first
        else:
            target_list += targets
    else:
        target_list += targets

    if len(target_list) == 0:
        result: CompletedProcess = CompletedProcess(args, 0)
    else:
        args += target_list
        args = [str(arg) for arg in args]

        try:
            result = process.run(args, env=env, **kwargs)
        except CalledProcessError as e:
            eprint(e)
            # print(f'gup returned {e.returncode}:')
            # print(f'stdout: {e.stdout}')
            # print(f'stderr: {e.stderr}')

            sys.exit(1)

    return result
