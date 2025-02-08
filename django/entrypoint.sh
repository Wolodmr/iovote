#!/bin/bash
set -e

# Ensure symbolic link exists at runtime
if [ ! -e /usr/bin/python ]; then
    ln -sf /usr/bin/python3 /usr/bin/python
fi

exec "$@"

