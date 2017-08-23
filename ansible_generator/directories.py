# -*- coding: utf-8 -*-
u"""directories is used to generate the necessary directory structures."""
from ansible_generator.log import setup_logger
from ansible_generator.utilities import join_cwd_and_directory_path

# python stdlib
from os.path import exists
from os import makedirs
from logging import INFO


def create_directory_layout(projects=None,
                            inventories=[u'production', u'staging'],
                            alternate_layout=False,
                            verbosity=INFO):
    u"""Creates the directory layout.

    Args:
        inventories: Array of strings noting the names of the inventories.
        alternate_layout: Boolean noting whether this is the primary or
            alternate directory structure.

    Returns:
        A boolean to say that it succeeded or failed.
    """
    logger = setup_logger(name=__name__, log_level=verbosity)
    if alternate_layout:
        required_paths = get_alternate_inventories_directory_paths(
            logger=logger, inventories=inventories)
    else:
        required_paths = [u'group_vars', u'host_vars', u'roles']

    logger.debug('msg="{n} required directories" directories="{p}"'.format(
        n=len(required_paths), p=required_paths))
    if projects:
        logger.debug(
            'msg="projects was defined" projects="{p}"'.format(p=projects))

        final_paths = []
        for project in projects:
            final_paths += [
                u'{project}/{path}'.format(project=project, path=required_path)
                for required_path in required_paths
            ]
        required_paths = final_paths
        logger.debug('msg="{n} project required directories" directories="{p}"'.
                     format(n=len(required_paths), p=required_paths))

    required_paths = map(join_cwd_and_directory_path, required_paths)

    for required_path in required_paths:
        success = create_directory(logger=logger, dir_path=required_path)
        if not success:
            return False

    return True


def create_directory(logger, dir_path):
    u"""Recursively creates a directory path if does not exist.

    Args:
        dir_path: The path to the directory that we would like created.

    Returns:
        A boolean to say that it was successful (True) or it failed (False).
    """
    if not exists(path=dir_path):
        try:
            logger.info('creating directory {dir}'.format(dir=dir_path))
            makedirs(dir_path)
        except Exception:
            logger.error(
                'failed to create {dir}'.format(dir=dir_path), exc_info=True)
            return False
    else:
        logger.info('directory {dir} exists'.format(dir=dir_path))
    return True


def get_alternate_inventories_directory_paths(logger, inventories):
    u"""

    Args:
         inventories: An array of string inventory names

    Returns:
        An array of directories that are required based on the provided
        inventory names.
    """
    logger.debug(u'msg="building alternate inventory layout directory paths"')
    inventory_paths = [u'roles']
    for inventory in inventories:
        inventory_paths.append(
            u'inventories/{inventory}/group_vars'.format(inventory=inventory))
        inventory_paths.append(
            u'inventories/{inventory}/host_vars'.format(inventory=inventory))
    return inventory_paths
