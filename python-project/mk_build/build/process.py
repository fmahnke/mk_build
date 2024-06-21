import os
import subprocess
from subprocess import (CalledProcessError,  # noqa: F401
    CompletedProcess)

import mk_build.config as config
import mk_build.log as log


def run(args, env=None, **kwargs) -> CompletedProcess:
    """ Execute a program in a child process. """

    args = [str(arg) for arg in args]

    if config.dry_run:
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
        env = os.environ

    for k, v in env.items():
        if k in exports:
            log.debug(f'    {k} = {v}')

    if config.dry_run:
        result: CompletedProcess = CompletedProcess(args, 0)
    else:
        result = subprocess.run(args, check=True, env=env, **kwargs)

    return result
