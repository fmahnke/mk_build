set -eu

. $srcdir/build/util.sh
. $srcdir/build/common_vars.sh

if [ "${GUP_XTRACE:-}" = 1 ]; then
    debug "$@"

    set -x
fi
