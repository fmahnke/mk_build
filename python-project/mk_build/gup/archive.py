#!/usr/bin/env python

from dataclasses import dataclass
import os
from typing import cast

from mk_build import exit, Target, build_dir, run
from mk_build.build.tools import ar
import mk_build.config as config


@dataclass
class Archive(Target):
    """ Builds archive files. """

    def update(self):
        super().update()

        args = [ar, 'rcs', config.get().output] + self.dependencies

        return run(args)


if __name__ == '__main__':
    dependencies = build_dir(os.environ['OBJECTS'].split())

    builder = Archive(dependencies=cast(list, dependencies))

    result = builder.update()

    exit(result)
