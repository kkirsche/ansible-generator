from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from logging import Logger
from typing import Union

from structlog.stdlib import BoundLogger


class CommandLineBuilder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @abstractproperty
    def logger(self) -> Union[Logger, BoundLogger]:
        """The logger instance for the command line builder."""
        pass

    @abstractmethod
    def _build_logger(
        self, level: str, json: bool, color: bool, debug: bool, quiet: bool, plain: bool
    ) -> None:
        """Build the logger property.

        Build the logger property, including configuring any required log handlers,
        output settings, etc.
        """
        pass

    @abstractmethod
    def _ensure_logger(self) -> None:
        """Ensure that the logger property was configured.

        This is a validation method used by the command line builder to verify that
        the order of events is being followed properly.
        """
        pass

    @abstractmethod
    def _build_parser(self) -> None:
        pass

    @abstractmethod
    def _ensure_parser(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def build(self) -> None:
        pass
