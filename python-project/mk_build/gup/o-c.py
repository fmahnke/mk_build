#!/usr/bin/env python

import os
import sys

import mk_build
from mk_build import *
import mk_build.config as config


def main(output=config.get().output, target=config.get().target,
         env=os.environ) -> int:
    print(f'o-c  {target}')

    ppflags = mk_build.environ('M_C_PPFLAGS', True).split()
    flags = mk_build.environ('M_C_FLAGS', True).split()
    deps = mk_build.environ('DEPS', True)

    if deps != '':
        gup(deps.split())

    source = path(top_source_dir(), path(target).with_suffix(''))

    # GCC manual recommends using -mgeneral-regs-only when functions are
    # no_caller_saved_registers

    cc = ['clang', '-target', 'i386-elf', '-march=i386', '-mgeneral-regs-only']

    args = cc + ppflags + flags + ['-c', '-o', output, source]

    gup(source)

    result = run(args)

    return result.returncode


if __name__ == '__main__':
    result = main()

    sys.exit(result)
