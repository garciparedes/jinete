"""Defines the hierarchy of exceptions raised when loading processes cannot be performed as expected."""

import logging

from ..exceptions import (
    JineteException,
)

logger = logging.getLogger(__name__)


class LoaderException(JineteException):
    """Loader exception class to be raised when loading processes cannot be performed as expected."""

    pass
