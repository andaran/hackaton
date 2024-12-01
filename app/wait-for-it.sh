#!/usr/bin/env bash
# wait-for-it.sh
# Используйте этот скрипт, чтобы ждать доступности хоста и порта.

set -e

TIMEOUT=15
QUIET=0
HOST=""
PORT=""

echoerr() {
    if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi
}

usage() {
    cat <<EOF
Usage:
  wait-for-it.sh host:port [-t timeout] [-- command args]
  -q | --quiet                        Не выводить сообщения
  -t TIMEOUT | --timeout=timeout      Время ожидания в секундах. По умолчанию: 15
  -- COMMAND ARGS                     Команда, которая будет выполнена после доступности хоста
EOF
    exit 1
}

wait_for() {
    for ((i=0;i<TIMEOUT;i++)); do
        if nc -z "$HOST" "$PORT" >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
    done
    echoerr "Timeout reached: $HOST:$PORT still not reachable"
    return 1
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            *:* )
                HOST=$(echo "$1" | cut -d: -f1)
                PORT=$(echo "$1" | cut -d: -f2)
                shift 1
                ;;
            -q|--quiet)
                QUIET=1
                shift 1
                ;;
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            --timeout=*)
                TIMEOUT="${1#*=}"
                shift 1
                ;;
            --)
                shift
                break
                ;;
            -*)
                echoerr "Unknown flag: $1"
                usage
                ;;
            *)
                break
                ;;
        esac
    done
}

parse_arguments "$@"
if [[ -z "$HOST" || -z "$PORT" ]]; then
    echoerr "Error: You must specify host and port to wait for."
    usage
fi

wait_for "$@"
if [[ $? -eq 0 ]]; then
    if [[ $# -gt 0 ]]; then
        exec "$@"
    fi
else
    exit 1
fi