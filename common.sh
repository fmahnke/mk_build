set -eu

output=${1:-}
target=${2:-}

debug() {
    printf 'pwd=%s\n' "$(pwd)"
    printf 'output path ($1)=%s\n' "$output"
    printf 'target ($2)=%s\n' "$target"
}

if [ "$GUP_XTRACE" = 1 ]; then
    debug "$@"

    set -x
fi

addprefix() {
    prefix="$1"
    shift

    result=

    for it in $@; do
        result="$prefix/$it $result"
    done

    printf "%s" "$result"
}

dir() {
    echo "${1%/*}"
}

ext() {
    echo "${1%.*}.$2"
}

: ${CFLAGS:=}
: ${M_CPPFLAGS:=}
