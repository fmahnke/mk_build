from collections.abc import MutableSequence
from os import PathLike
from pathlib import Path
from typing import TypeAlias

PathInput: TypeAlias = Path | PathLike | str
PathInputs: TypeAlias = PathInput | MutableSequence[PathInput]
Paths: TypeAlias = Path | MutableSequence[Path]

__all__ = [
    'Path',
    'PathInput'
]


def suffix(paths: Paths, new_ext: str) -> Paths:
    """ Replace the suffix in path or paths. """

    if isinstance(paths, MutableSequence):
        return [it.with_suffix(new_ext) for it in paths]
    else:
        return paths.with_suffix(new_ext)


def path(*path_segments: PathInput) -> Path:
    """ Create a Path from path_segments. """

    return Path(*path_segments)


def paths(paths: tuple[Path]) -> MutableSequence[Path]:
    """ Convert paths to a list of Path. """

    return [Path(it) for it in paths]


def name(path: PathInput) -> Path:
    return Path(Path(path).name)


def path_dir(path: Path) -> Path:
    return path.parents[0]
