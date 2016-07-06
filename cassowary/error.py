from __future__ import print_function, unicode_literals, absolute_import, division


class BaseException(Exception):
    pass


class InternalError(BaseException):
    pass


class ConstraintNotFound(BaseException):
    pass


class RequiredFailure(BaseException):
    pass
