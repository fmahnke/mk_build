import os
import subprocess
from subprocess import CalledProcessError, CompletedProcess
import sys
from typing import Any, Optional, Sequence

import mk_build.config as __config
import mk_build.log as log
from mk_build.util.io import eprint

__all__ = ['CalledProcessError', 'CompletedProcess', 'run']

_config = __config.get()


def run(
    args: Sequence[Any],
    env: Optional[dict[str, str]] = None,
    **kwargs: Any
) -> CompletedProcess[bytes]:
    """ Execute a program in a child process. """

    args = [str(arg) for arg in args]

    if _config.dry_run:
        dry = ' (dry run)'
    else:
        dry = ''

    log.info(f"run: {' '.join(args)}{dry}")

    exports = [
        'M_ASM_PPFLAGS',
        'DEPS'
    ]

    if env is not None:
        env = env | os.environ
    else:
        env = dict(os.environ)

    for k, v in env.items():
        if k in exports:
            log.debug(f'    {k} = {v}')

    if _config.dry_run:
        result: CompletedProcess[bytes] = CompletedProcess(args, 0)
    else:
        try:
            result = subprocess.run(args, check=True, env=env, **kwargs)
        except CalledProcessError as e:
            eprint(e)

            sys.exit(e.returncode)

    return result
