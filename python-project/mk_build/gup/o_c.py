#!/usr/bin/env python

from dataclasses import dataclass

from mk_build import *
from mk_build.build.path import Path
import mk_build.config as config


@dataclass
class ObjectFromC(Target):
    def update(self) -> CompletedProcess[bytes]:
        super().update()

        ppflags = ensure_type(environ('M_C_PPFLAGS', ''), str).split()
        ppflags.append(f'-I{Path(top_source_dir(), source_dir())}')
        flags = ensure_type(environ('M_C_FLAGS', ''), str).split()
        deps = ensure_type(environ('DEPS', ''), str)

        if deps != '':
            gup(deps.split())

        source = Path(
            top_source_dir(),
            path(ensure_type(config.get().target, Path)).with_suffix('')
        )

        cc = [tools.cc]

        args = cc + ppflags + flags + ['-c', '-o', config.get().output, source]

        gup(source)

        return run(args)


if __name__ == '__main__':
    builder = ObjectFromC()

    result = builder.update()

    exit(result)
