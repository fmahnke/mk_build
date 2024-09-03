#!/usr/bin/env python

from dataclasses import dataclass
import os

from mk_build import CompletedProcess, Target, exit, run
from mk_build.build import build_dir_add
from mk_build.build.tools import ar
import mk_build.config as config


@dataclass
class Archive(Target):
    """ Builds archive files. """

    def update(self) -> CompletedProcess[bytes]:
        super().update()

        args = [ar, 'rcs', config.get().output] + self.dependencies

        return run(args)


def main():
    dependencies = build_dir_add(os.environ['OBJECTS'].split())

    builder = Archive(dependencies=list(dependencies))

    result = builder.update()

    exit(result)


if __name__ == '__main__':
    main()
