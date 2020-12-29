"""The ansible_generator.core module defines cross-sectional application code.
The purpose of the core module is to provide a consistent access pattern to all aspects
of the platform to critical data. To avoid issues with drift between different systems,
we unify these into a single module which can be re-used between the other modules.
"""
from ansible_generator.core.log_filters import InfoFilter
from ansible_generator.core.log_protocol import LoggerProtocol
from ansible_generator.core.version import version, version_tuple

__all__ = ["version", "version_tuple", "InfoFilter", "LoggerProtocol"]
