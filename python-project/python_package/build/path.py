from pathlib import PurePath

def ext(path, new_ext):
    index = path.rfind('.')
    return path[:index + 1] + new_ext

def path(*path_segments):
    return PurePath(*path_segments)

def paths(paths):
    return [PurePath(it) for it in paths]

def name(path):
    return PurePath(PurePath(path).name)

def path_dir(path):
    return path.parents[0]
