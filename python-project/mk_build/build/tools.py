import os
from subprocess import CompletedProcess

from mk_build.build.process import run

if 'CC' in os.environ:
    cc = os.environ['CC']
else:
    cc = 'gcc'

if 'LINK' in os.environ:
    link = os.environ['LINK']
else:
    link = 'ld'

if 'NM' in os.environ:
    nm = os.environ['NM']
else:
    nm = 'nm'

if 'OBJDUMP' in os.environ:
    objdump = os.environ['OBJDUMP']
else:
    objdump = 'objdump'


def run_link(args: list) -> CompletedProcess:
    return run([link] + args)
