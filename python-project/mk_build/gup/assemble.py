#!/usr/bin/env python

from dataclasses import dataclass

from mk_build import *
import mk_build.config as config_

config = config_.get()


@dataclass
class Assemble(Target):
    def update(self) -> CompletedProcess[bytes]:
        super().update()

        m_asm_ppflags = ensure_type(environ('M_ASM_PPFLAGS', ''), str).split()
        m_asm_ppflags.append(f'-I{source_dir_abs()}')

        deps = ensure_type(environ('DEPS', ''), str)

        if deps != '':
            gup(deps.split())

        source = path(
            top_source_dir(),
            path(ensure_type(config.target, Path)).with_suffix('')
        )

        args = (
            [tools.asm]
            + ['-f', 'elf32', '-g', '-w+error']
            + m_asm_ppflags
            + ['-o', config.output, source]
        )

        gup(source)

        return run(args)


if __name__ == '__main__':
    builder = Assemble()

    result = builder.update()

    exit(result)
