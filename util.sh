debug() {
    printf 'pwd=%s\n' "$(pwd)"
    printf 'output path ($1)=%s\n' "$output"
    printf 'target ($2)=%s\n' "$target"
}

# addprefix PREFIX ITEMS...
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

not_dir() {
    echo "${1##*/}"
}

ext() {
    echo "${1%.*}.$2"
}
