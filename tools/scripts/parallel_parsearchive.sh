#!/bin/bash
# Patchwork - automated patch tracking system
# Copyright (C) 2018 Daniel Axtens <dja@axtens.net>
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

set -euo pipefail

usage() {
    cat <<EOF
parallel_parsearchive.sh - load archives in parallel
Usage:
  parallel_parsearchive.sh [parsearchive options] -- <archives>
  The -- is mandatory.
  As many processes as there are archives will be spun up.

Example:
  tools/scripts/parallel_parsearchive.sh --list-id=patchwork.ozlabs.org -- foo-*
EOF
    exit 1
}

if [ $# -eq 0 ] || [[ $1 == "-h" ]]; then
    usage;
fi

PARSEARCHIVE_OPTIONS=""
while [[ $1 != "--" ]]; do
    PARSEARCHIVE_OPTIONS="$PARSEARCHIVE_OPTIONS $1"
    shift
    if [ $# -eq 0 ]; then
        usage;
    fi
done
shift

if [ $# -eq 0 ]; then
    usage;
fi

set +u
if [ -z "$PW_PYTHON" ]; then
    PW_PYTHON=python3
fi
set -u

for x in "$@"; do
    echo "Starting $x"
    "$PW_PYTHON" manage.py parsearchive $PARSEARCHIVE_OPTIONS "$x" &
done
echo "Processes started in the background."
