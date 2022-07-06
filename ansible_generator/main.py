# -*- coding: utf-8 -*-
"""main defines the entrypoint into the application."""
from logging import INFO, Logger
from typing import MutableSequence, Union

from ansible_generator.directories import create_directory_layout
from ansible_generator.files import create_file_layout
from ansible_generator.log import setup_logger


class AnsibleGenerator:
    projects: MutableSequence[str]
    inventories: MutableSequence[str]
    roles: MutableSequence[str]

    alternate_layout: bool
    verbosity: int
    logger: Logger

    def __init__(
        self,
        inventories: Union[MutableSequence[str], None] = None,
        projects: Union[MutableSequence[str], None] = None,
        roles: Union[MutableSequence[str], None] = None,
        alternate_layout: bool = False,
        verbosity: int = INFO,
    ) -> None:
        if projects is None:
            projects = []
        if inventories is None:
            inventories = ["production", "staging"]
        if roles is None:
            roles = []

        self.verbosity = verbosity
        self.logger = setup_logger(name=__name__, log_level=self.verbosity)
        self.logger.debug(
            (
                'msg="initializing generator" inventories="%s" '
                + 'alternate_layout="%s" projects="%s"'
            ),
            ", ".join(inventories),
            alternate_layout,
            ", ".join(projects),
        )
        self.projects = projects
        self.inventories = inventories
        self.alternate_layout = alternate_layout
        self.roles = roles

    def run(self) -> None:
        self.logger.debug('msg="beginning create directory"')
        if create_directory_layout(
            projects=self.projects,
            inventories=self.inventories,
            alternate_layout=self.alternate_layout,
            verbosity=self.verbosity,
        ):
            create_file_layout(
                projects=self.projects,
                inventories=self.inventories,
                alternate_layout=self.alternate_layout,
                roles=self.roles,
                verbosity=self.verbosity,
            )
