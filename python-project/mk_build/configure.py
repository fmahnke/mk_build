import os

from mk_build.config import *
import mk_build.log as log


def main():
    if 'source_dir' not in os.environ:
        source_dir = 'crap'
        log.info('Auto-detected source directory: {source_dir}')

    if 'build_dir' not in os.environ:
        build_dir = os.getcwd()
        log.info('Auto-detected build directory: {build_dir}')

    config_file = ConfigFile(source_dir, build_dir)


if __name__ == '__main__':
    main()

'''
fi

if [ -z "${builddir:-}" ]; then
    builddir="$(pwd)"
    printf 'Auto-detected build directory: builddir=%s\n' "$builddir"
fi

printf "srcdir=%s\n" "$srcdir" > "$builddir/config.sh"
printf "builddir=%s\n" "$builddir" >> "$builddir/config.sh"
'''
