from pathlib import PurePath


def suffix(paths: PurePath | list[PurePath],
           new_ext) -> PurePath | list[PurePath]:
    """ Replace the suffix in path or paths. """

    if isinstance(paths, list):
        return [it.with_suffix(new_ext) for it in paths]
    else:
        return paths.with_suffix(new_ext)


def path(*path_segments) -> PurePath:
    """ Create a PurePath from path_segments. """

    return PurePath(*path_segments)


def paths(paths) -> list[PurePath]:
    """ Convert paths to a list of PurePath. """

    return [PurePath(it) for it in paths]


def name(path) -> PurePath:
    return PurePath(PurePath(path).name)


def path_dir(path: PurePath) -> PurePath:
    return path.parents[0]
