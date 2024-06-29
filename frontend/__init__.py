# Copyright (c) TaKo AI Sp. z o.o.

from importlib import metadata

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = ""
del metadata
