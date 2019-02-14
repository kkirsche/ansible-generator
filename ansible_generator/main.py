# -*- coding: utf-8 -*-
"""main defines the entrypoint into the application."""
from ansible_generator.files import create_file_layout
from ansible_generator.directories import create_directory_layout
from ansible_generator.log import setup_logger
from logging import INFO


class AnsibleGenerator(object):
    def __init__(
        self,
        projects=None,
        inventories=["production", "staging"],
        alternate_layout=False,
        roles=[],
        verbosity=INFO,
    ):
        super(self.__class__, self).__init__()
        self.verbosity = verbosity
        self.logger = setup_logger(name=__name__, log_level=self.verbosity)
        self.logger.debug(
            (
                'msg="initializing generator" inventories="{inv}" '
                'alternate_layout="{alt}" projects="{proj}"'
            ).format(inv=inventories, alt=alternate_layout, proj=", ".join(projects))
        )
        self.projects = projects
        self.inventories = inventories
        self.alternate_layout = alternate_layout
        self.roles = roles

    def run(self):
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
