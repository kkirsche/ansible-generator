# -*- coding: utf-8 -*-
u"""Create a logger instance """
# third party packages
from raven import Client, fetch_package_version
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

# python stdlib
import logging


def get_sentry_handler():
    client = Client(
        dsn=(u'https://036bd28e074a4a4a99712dc05c9f768e:d4bbdc0c3ca7495aa2bb4a'
             u'cf1ba25d88@sentry.io/202195'),
        release=fetch_package_version('ansible-generator'))
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    return handler


def setup_logger(name, log_level=logging.INFO):
    log_format = '%(message)s'
    logging.basicConfig(format=log_format)
    handler = get_sentry_handler()
    setup_logging(handler)
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
