. $srcdir/build/util.sh

if [ -z "${common_sourced:-}" ]; then

common_sourced=1

export PATH="$srcdir/build:$PATH"

output=${1:-}
target=${2:-}

#: ${output:="${1:-}"}
#: ${target:="${2:-}"}
#export output
#export target

config_dir="$(pwd)"

while true; do
    config_path="$config_dir/config.sh"

    if [ -f "$config_path" ]; then
        . "$config_path"
        break
    fi

    if [ "$config_dir" = "${GUP_ROOT:-}" ]; then
        echo "error: config not found"
        exit 1
    fi

    config_dir="$(dir $config_dir)"
done

unset config_dir
unset config_path

: ${CFLAGS:=}
: ${M_CPPFLAGS:=}
: ${M_LDFLAGS:=}

if [ -f "$srcdir/build/vars.sh" ]; then
    . "$srcdir/build/vars.sh"
fi

fi  # if [ -z "${common_sourced:-}" ]
