#!/usr/bin/env python

from collections.abc import Sequence
from dataclasses import dataclass, field
import os

from mk_build import exit, Target, run
from mk_build.build.path import PathInput
from mk_build.build.tools import cc
import mk_build.config as config
from ..build import build_dir_add


@dataclass
class CCompileAndLink(Target):
    libraries: Sequence[PathInput] = field(default_factory=list)

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
    dependencies = build_dir_add(os.environ['OBJECTS'].split())

    builder = CCompileAndLink(dependencies=dependencies)

    result = builder.update()

    exit(result)
