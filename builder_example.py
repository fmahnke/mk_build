#!/usr/bin/env python

import os

from mk_build import *


def main(output, target, env=os.environ) -> int:
    print(f'bin  {target}')

    '''
    Program options from the environment.

    m_ldflags = env['M_LDFLAGS']
    '''

    '''
    Source files from the environment.

    sources = env['SRCS']
    '''

    '''
    Object files from the environment.

    objects = env['OBJS']
    '''

    '''
    Build command

    args = ['i686-elf-ld', '-o', output, *m_ldflags, *objects]
    '''

    '''
    Capturing and redirecting output.

    result = run(args, capture_output=True)

    with open(output, 'wb') as fi:
        fi.write(result.stdout)
    '''

    '''
    Always return the result. Zero indicates success.

    return run(args).returncode
    '''

    return 0


'''
Script entry point is required if the builder is called directly by gup.

import sys

if __name__ == '__main__':
    result = main(output, target)

    sys.exit(result)
'''
