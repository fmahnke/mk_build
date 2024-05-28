from pathlib import PurePath
from typing import Dict


class Deps:
    def __init__(self, path, build_dir) -> None:
        self.build_dir = build_dir
        self.files: Dict[str, list[str]] = {}

        with open(path) as fi:
            lines = fi.readlines()

        for line in lines:
            line = line.strip()
            fields = line.split()

            if line.startswith('file'):
                path = PurePath(fields[-1])

                if path.suffix not in self.files:
                    self.files[path.suffix] = []

                self.files[path.suffix].append(path)

    def files_str(self, suffix) -> str:
        return ' '.join([f'{self.build_dir}/{it}'
            for it in self.files[suffix]])

    def files_list(self, suffix) -> list:
        return [f'{self.build_dir}/{it}' for it in self.files[suffix]]
