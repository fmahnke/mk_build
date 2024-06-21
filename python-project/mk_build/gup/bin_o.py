#!/usr/bin/env python

import os
import sys

from mk_build import *
import mk_build.config as config


def main(output=config.get().output, target=config.get().target,
         env=os.environ) -> int:
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


if __name__ == '__main__':
    result = main()

    sys.exit(result)
