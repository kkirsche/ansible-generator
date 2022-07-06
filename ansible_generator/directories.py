"""directories is used to generate the necessary directory structures."""
from logging import INFO, Logger
from pathlib import Path
from typing import Iterable, MutableSequence, Set, Union

from ansible_generator.log import setup_logger
from ansible_generator.utilities import join_cwd_and_directory_path


def create_directory_layout(
    projects: Iterable[str],
    inventories: MutableSequence[str],
    alternate_layout: bool = False,
    verbosity: int = INFO,
) -> bool:
    """Creates the directory layout.

    Args:
        inventories: Array of strings noting the names of the inventories.
        alternate_layout: Boolean noting whether this is the primary or
            alternate directory structure.

    Returns:
        A boolean to say that it succeeded or failed.
    """
    logger = setup_logger(name=__name__, log_level=verbosity)
    for itemNum, inventory in enumerate(inventories):
        inventories[itemNum] = inventory.split("/")[-1]
        if inventory == ".":
            inventories[itemNum] = "dot"
        if inventory == "..":
            inventories[itemNum] = "dotdot"
        if inventory == "*":
            inventories[itemNum] = "star"

    if alternate_layout:
        required_paths = get_alternate_inventories_directory_paths(
            logger=logger, inventories=inventories
        )
    else:
        required_paths = {"group_vars", "host_vars", "roles"}

    logger.debug(
        'msg="%s required directories" directories="%s"',
        len(required_paths),
        ", ".join(required_paths),
    )
    if projects:
        logger.debug('msg="projects was defined" projects="%s"', ", ".join(projects))

        final_paths: Set[str] = set()
        for project in projects:
            final_paths.update(
                f"{project}/{required_path}" for required_path in required_paths
            )
        required_paths = final_paths
        logger.debug(
            'msg="%s project required directories" directories="%s"',
            len(required_paths),
            ", ".join(required_paths),
        )

    create_paths = set(map(join_cwd_and_directory_path, required_paths))
    for cp in create_paths:
        success = create_directory(logger=logger, dir_path=cp)
        if not success:
            return False

    return True


def create_directory(logger: Logger, dir_path: Union[Path, str]) -> bool:
    """Recursively creates a directory path if does not exist.

    Args:
        dir_path: The path to the directory that we would like created.

    Returns:
        A boolean to say that it was successful (True) or it failed (False).
    """
    if not isinstance(dir_path, Path):
        dir_path = Path(dir_path)

    if dir_path.exists():
        logger.info("directory %s exists", dir_path)
        return True

    try:
        logger.info("creating directory %s", dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        logger.error(
            (
                "PermissionError: failed to create %s\n"
                + "Try using sudo to fix the issue 😃"
            ),
            dir_path,
        )
    except Exception:
        logger.error("failed to create %s", dir_path, exc_info=True)
    return False


def get_alternate_inventories_directory_paths(
    logger: Logger, inventories: Iterable[str]
) -> Set[str]:
    """

    Args:
         inventories: An array of string inventory names

    Returns:
        An array of directories that are required based on the provided
        inventory names.
    """
    logger.debug('msg="building alternate inventory layout directory paths"')
    inventory_paths = {"roles"}
    for inventory in inventories:
        inventory_paths.update(
            {
                f"inventories/{inventory}/group_vars",
                f"inventories/{inventory}/host_vars",
            }
        )
    return inventory_paths
