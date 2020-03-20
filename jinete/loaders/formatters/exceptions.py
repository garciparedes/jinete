"""Defines the hierarchy of exceptions raised when load formatting processes cannot be performed as expected."""

import logging

from ..exceptions import (
    LoaderException,
)

logger = logging.getLogger(__name__)


class LoaderFormatterException(LoaderException):
    """Loader exception class to be raised when loading processes cannot be performed as expected."""

    pass
