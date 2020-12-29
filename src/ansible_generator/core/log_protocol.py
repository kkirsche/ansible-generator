"""The ansible_generator.core.log_protocol module defines a generic log protocol.
This log protocol is defined to simplify the use of different logging
libraries. Instead of chasing a large Union[Logger, BoundLogger, ...] statement,
this takes the approach of using duck typing (if it quacks, it's a duck) to say
as long as the item we receive has the following methods, whose signatures have
been taking from logging.Logger, that's all we need.
"""
from typing import Protocol


class LoggerProtocol(Protocol):
    """LoggerProtocol defines the method protocol for a logger."""

    def debug(self, msg: str, *args, **kwargs) -> None:
        """Debug log level messages."""
        ...

    def info(self, msg: str, *args, **kwargs) -> None:
        """Informational log level messages."""
        ...

    def warning(self, msg: str, *args, **kwargs) -> None:
        """Warning log level messages.
        While logging.warn does exist, that method is deprecated, as such we do not
        model it.
        """
        ...

    def error(self, msg: str, *args, **kwargs) -> None:
        """Error log level messages."""
        ...

    def critical(self, msg: str, *args, **kwargs) -> None:
        """Critical log level messages."""
        ...

    def log(self, msg: str, *args, **kwargs) -> None:
        """General log messages."""
        ...

    def exception(self, msg: str, *args, **kwargs) -> None:
        """Exception handler log messages."""
        ...
