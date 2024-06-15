from pathlib import Path


def suffix(paths: Path | list[Path],
           new_ext) -> Path | list[Path]:
    """ Replace the suffix in path or paths. """

    if isinstance(paths, list):
        return [it.with_suffix(new_ext) for it in paths]
    else:
        return paths.with_suffix(new_ext)


def path(*path_segments) -> Path:
    """ Create a Path from path_segments. """

    return Path(*path_segments)


def paths(paths) -> list[Path]:
    """ Convert paths to a list of Path. """

    return [Path(it) for it in paths]


def name(path) -> Path:
    return Path(Path(path).name)


def path_dir(path: Path) -> Path:
    return path.parents[0]
