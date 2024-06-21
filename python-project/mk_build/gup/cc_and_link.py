#!/usr/bin/env python

from collections.abc import MutableSequence
from dataclasses import dataclass, field
import os
from typing import cast

from mk_build import exit, Target, build_dir, run
from mk_build.build.path import PathInput
from mk_build.build.tools import cc
import mk_build.config as config


@dataclass
class CCompileAndLink(Target):
    libraries: MutableSequence[PathInput] = field(default_factory=list)

    def update(self):
        super().update()

        args = (
            [cc]
            + ['-o', config.get().output]
            + self.dependencies
            + ['-l' + i for i in self.libraries]
        )

        return run(args)


if __name__ == '__main__':
    dependencies = build_dir(os.environ['OBJECTS'].split())

    builder = CCompileAndLink(dependencies=cast(list, dependencies))

    result = builder.update()

    exit(result)
