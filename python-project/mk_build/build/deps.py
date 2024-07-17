from typing import Dict

from .path import Path, PathInput


class Deps:
    def __init__(self, path: PathInput, build_dir: PathInput) -> None:
        self.build_dir = build_dir
        self.files: Dict[str, list[str]] = {}

        with open(path) as fi:
            lines = fi.readlines()

        for line in lines:
            line = line.strip()
            fields = line.split()

            if line.startswith('file'):
                path = Path(fields[-1])

                if path.suffix not in self.files:
                    self.files[path.suffix] = []

                self.files[path.suffix].append(str(path))

    def files_str(self, suffix: str) -> str:
        return ' '.join([f'{self.build_dir}/{it}'
            for it in self.files[suffix]])

    def files_list(self, suffix: str) -> list[str]:
        return [f'{self.build_dir}/{it}' for it in self.files[suffix]]
