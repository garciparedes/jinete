import logging

from ..exceptions import (
    JineteException,
)

logger = logging.getLogger(__name__)


class LoaderException(JineteException):
    pass
