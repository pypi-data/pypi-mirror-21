# -*- coding: utf-8 -*-

import sys

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

PY2 = sys.version_info[0] == 2
PY3K = sys.version_info[0] >= 3

if PY2:
    unicode = unicode
    basestring = basestring
else:
    unicode = str
    basestring = str


def decode(string, encodings=None):
    if not PY2 and not isinstance(string, bytes):
        return string

    if PY2 and isinstance(string, unicode):
        return string

    if encodings is None:
        encodings = ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.decode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return string.decode(encodings[0], errors='ignore')


def encode(string, encodings=None):
    if not PY2 and isinstance(string, bytes):
        return string

    if PY2 and isinstance(string, str):
        return string

    if encodings is None:
        encodings = ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.encode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return string.encode(encodings[0], errors='ignore')
