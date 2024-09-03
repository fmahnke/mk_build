#!/usr/bin/env python

import os
import sys
from typing import Optional

from mk_build import *
import mk_build.config as config


def main(
    output: Optional[Path] = config.get().output,
    target: Optional[Path] = config.get().target,
    env: dict[str, str] = dict(os.environ)
) -> int:
    print(f'bin  {target}')

    m_ldflags = env['M_LDFLAGS']

    objects = env['OBJS']

    gup(objects)

    # .bin target

    result = run([tools.link, '-o', output, *m_ldflags, *objects])

    if result.returncode != 0:
        return result.returncode

    # bin.nm target

    result = run([tools.nm, '-S', '-n', output], capture_output=True)

    if result.returncode != 0:
        return result.returncode

    with open(f'{os.getcwd()}/{target}.nm', 'wb') as fi:
        fi.write(result.stdout)

    # bin.dasm target

    result = run([tools.objdump, '-M', 'intel',
                 '-d', output], capture_output=True)

    if result.returncode != 0:
        return result.returncode

    with open(f'{os.getcwd()}/{target}.dasm', 'wb') as fi:
        fi.write(result.stdout)

    return 0


def main1():
    result = main1()

    sys.exit(result)


if __name__ == '__main__':
    main1()
