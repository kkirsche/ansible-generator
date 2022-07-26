"""Create a logger instance """
from logging import ERROR, INFO, Logger, basicConfig, getLogger
from os import getenv
from typing import Union

from sentry_sdk import init
from sentry_sdk.integrations.logging import LoggingIntegration

from ansible_generator.version import __version__


def configure_sentry() -> None:
    """Configure the Sentry telemetry, unless disabled."""
    disabled = getenv(key="DISABLE_ANSIBLE_GENERATE_TELEMETRY", default=False)
    if not disabled:
        sentry_logging = LoggingIntegration(level=INFO, event_level=ERROR)
        init(
            dsn="https://036bd28e074a4a4a99712dc05c9f768e@sentry.io/202195",
            integrations=[sentry_logging],
            release=__version__,
        )


def setup_logger(name: Union[str, None] = None, log_level: int = INFO) -> Logger:
    """Setup a new Logger instance.

    Args:
        name (optional): The name of the logger. Usually ``__file__`. Defaults to None.
        log_level (optional): THe logging level to use. Defaults to INFO.

    Returns:
        Logger: The configured logger.
    """
    log_format = "%(message)s"
    basicConfig(format=log_format)
    configure_sentry()
    logger = getLogger(name)
    logger.setLevel(log_level)
    return logger
