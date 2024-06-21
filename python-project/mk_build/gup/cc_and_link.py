#!/usr/bin/env python

from dataclasses import dataclass, field
import os

from mk_build import Paths, Target, build_dir, paths, run
from mk_build.build.tools import cc
import mk_build.config as config


@dataclass
class CCompileAndLink(Target):
    libraries: Paths = field(default_factory=list)

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
    dependencies = paths(build_dir(os.environ['OBJECTS'].split()))

    builder = CCompileAndLink(dependencies=dependencies)

    result = builder.update()

    exit(result)
