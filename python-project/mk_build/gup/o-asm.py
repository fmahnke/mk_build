#!/usr/bin/env python

import os
import sys

import mk_build
from mk_build import *
import mk_build.config as config


def main(output=config.get().output, target=config.get().target,
         env=os.environ) -> int:
    print(f'o-asm  {target}')

    m_asm_ppflags = mk_build.environ('M_ASM_PPFLAGS', True)
    deps = mk_build.environ('DEPS', True)

    if deps != '':
        gup(deps.split())

    source = path(top_source_dir(), path(target).with_suffix('.asm'))

    target_source_dir = path_dir(source)

    args = ['nasm', '-f', 'elf32', '-g', '-w+error', '-i', target_source_dir,
        m_asm_ppflags, '-o', output, source]

    gup(source)

    result = run(args)

    return result.returncode


if __name__ == '__main__':
    result = main()

    sys.exit(result)
