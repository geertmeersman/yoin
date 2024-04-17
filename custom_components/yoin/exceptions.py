"""Exceptions used by Yoin."""


class YoinException(Exception):
    """Base class for all exceptions raised by Yoin."""

    pass


class YoinServiceException(Exception):
    """Raised when service is not available."""

    pass


class BadCredentialsException(Exception):
    """Raised when credentials are incorrect."""

    pass


class NotAuthenticatedException(Exception):
    """Raised when session is invalid."""

    pass


class GatewayTimeoutException(YoinServiceException):
    """Raised when server times out."""

    pass


class BadGatewayException(YoinServiceException):
    """Raised when server returns Bad Gateway."""

    pass
