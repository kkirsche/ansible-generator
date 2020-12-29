"""The ansible_generator.core.log_filters module defines filters for various log levels.
These are applied to log handlers to ensure that they only log certain log
levels.
"""
from logging import WARNING, Filter, LogRecord


class InfoFilter(Filter):
    """InfoFilter is used to filter log messages which are only informational."""

    def filter(self, record: LogRecord) -> bool:
        """
        There are two different ways to implement this. First, like we have,
        second is to use:
            >>> return record.levelno in (DEBUG, INFO)
        While this works, it is limited to those values, and does not support
        custom log levels which a user has defined between the official ones.
        We instead have taken the approach of saying the official level goes
        from INFO to WARNING, as such, anything less than a WARNING is still
        INFO level.
        """
        # return record.levelno in (DEBUG, INFO)
        return record.levelno < WARNING
