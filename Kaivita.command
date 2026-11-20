#!/bin/sh

cd -- "$(dirname -- "$0")" || exit 1
# Finderist käivitades ei pruugi Pythoni paigalduskaustad PATH-is olla.
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

if ! command -v python3 >/dev/null 2>&1 || ! python3 -c 'import tkinter'; then
    printf '%s\n' 'Paigalda Python 3 koos Tkinteriga: https://www.python.org/downloads/macos/' >&2
    exit 1
fi

exec python3 mootor.py
