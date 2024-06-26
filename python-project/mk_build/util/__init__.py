import os.path
import platform


def system():
    # TODO may not actually need this

    if os.path.isfile('/proc/sys/fs/binfmt_misc/WSLInterop'):
        return 'wsl'
    else:
        return platform.system()
