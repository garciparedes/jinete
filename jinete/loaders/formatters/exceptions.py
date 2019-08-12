import logging

from ..exceptions import (
    LoaderException,
)

logger = logging.getLogger(__name__)


class LoaderFormatterException(LoaderException):
    pass
