# -*- coding: utf-8 -*-
"""utilities are functions that need to be used by multiple files."""
from ansible_generator.log import setup_logger
from os.path import join
from os import getcwd

logger = setup_logger(name=__name__)


def join_cwd_and_directory_path(dir_path):
    logger.debug("joining paths")
    cwd = getcwd()
    joined_path = join(cwd, dir_path)
    return joined_path
