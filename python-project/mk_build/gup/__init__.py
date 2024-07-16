import os
from typing import Any, Optional, Iterable

from mk_build.build.path import Path, PathInput
import mk_build.build.process as process
from mk_build.build.process import CompletedProcess
from mk_build.config import config


def gup_path(path: PathInput) -> Optional[Path]:
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


def gup(
    *targets: PathInput | Iterable[PathInput],
    env: Optional[dict[str, str]] = None,
    **kwargs: Any
) -> Optional[CompletedProcess]:
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

        result = process.run(args, env=env, **kwargs)

    return result
