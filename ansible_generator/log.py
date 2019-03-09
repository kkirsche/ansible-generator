# -*- coding: utf-8 -*-
"""Create a logger instance """
# third party packages
from sentry_sdk import init
from sentry_sdk.integrations.logging import LoggingIntegration

# python stdlib
from pkg_resources import get_distribution
import logging


def configure_sentry():
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
    init(
        dsn="https://036bd28e074a4a4a99712dc05c9f768e@sentry.io/202195",
        integrations=[sentry_logging],
        release=get_distribution("ansible-generator").version,
    )


def setup_logger(name, log_level=logging.INFO):
    log_format = "%(message)s"
    logging.basicConfig(format=log_format)
    configure_sentry()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
