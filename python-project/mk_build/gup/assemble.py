#!/usr/bin/env python

from dataclasses import dataclass

from mk_build import *
import mk_build.config as config_

config = config_.get()


@dataclass
class Assemble(Target):
    def update(self):
        super().update()

        m_asm_ppflags = environ('M_ASM_PPFLAGS', '').split()
        m_asm_ppflags.append(f'-I{source_dir_abs()}')

        deps = environ('DEPS', '')

        if deps != '':
            gup(deps.split())

        source = path(top_source_dir(),
                      path(config.target).with_suffix(''))

        args = (
            [tools.asm]
            + ['-f', 'elf32', '-g', '-w+error']
            + m_asm_ppflags
            + ['-o', config.output, source]
        )

        gup(source)

        result = run(args)

        return result.returncode


if __name__ == '__main__':
    builder = Assemble()

    result = builder.update()

    exit(result)
