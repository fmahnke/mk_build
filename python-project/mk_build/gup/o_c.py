#!/usr/bin/env python

from dataclasses import dataclass

import mk_build
from mk_build import *
from mk_build.build.path import Path
import mk_build.config as config


@dataclass
class ObjectFromC(Target):
    def update(self):
        super().update()

        ppflags = mk_build.environ('M_C_PPFLAGS', '').split()
        ppflags.append(f'-I{Path(top_source_dir(), source_dir())}')
        flags = mk_build.environ('M_C_FLAGS', '').split()
        deps = mk_build.environ('DEPS', '')

        if deps != '':
            gup(deps.split())

        source = Path(top_source_dir(),
                      path(config.get().target).with_suffix(''))

        cc = [tools.cc]

        args = cc + ppflags + flags + ['-c', '-o', config.get().output, source]

        gup(source)

        result = run(args)

        return result.returncode


if __name__ == '__main__':
    builder = ObjectFromC()

    result = builder.update()

    exit(result)
