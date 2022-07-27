"""files is used to generate the necessary file."""
from logging import INFO, Logger
from os import PathLike, utime
from pathlib import Path
from shlex import split
from shutil import which
from subprocess import Popen  # nosec
from tempfile import TemporaryFile
from typing import Collection, Iterable, MutableSequence, Set, Tuple, Union

from ansible_generator.log import setup_logger
from ansible_generator.utilities import join_cwd_and_directory_path

StrOrBytesPath = Union[str, bytes, PathLike[str], PathLike[bytes]]


def create_file_layout(
    projects: Collection[str],
    inventories: MutableSequence[str],
    roles: MutableSequence[str],
    alternate_layout: bool = False,
    verbosity: int = INFO,
) -> bool:
    """Create the file layout for the inputs.

    Args:
        projects: An iterable of project names.
        inventories: A mutable sequence of inventories.
        roles: A mutable sequence of roles.
        alternate_layout (optional): Use the alternate layout. Defaults to False.
        verbosity (optional): The logging level. Defaults to INFO.

    Returns:
        bool: True if the layout was created successfully, False otherwise.
    """
    logger = setup_logger(name=__name__, log_level=verbosity)
    minimum_paths = ["site.yml"]

    for itemNum, inventory in enumerate(inventories):
        inventories[itemNum] = inventory.split("/")[-1]
        if inventory == ".":
            inventories[itemNum] = "dot"
        if inventory == "..":
            inventories[itemNum] = "dotdot"
        if inventory == "*":
            inventories[itemNum] = "star"

    required_paths = set(minimum_paths)
    if alternate_layout:
        required_paths.update(
            get_alternate_inventories_file_paths(logger=logger, inventories=inventories)
        )
        required_paths.update(minimum_paths)
    else:
        required_paths.update(inventories)

    logger.debug(
        'msg="%s required files" files="%s"', len(required_paths), required_paths
    )

    if projects:
        logger.debug('msg="projects was defined" projects="%s"', projects)

        final_paths: Set[str] = set()
        for project in projects:
            final_paths.update(
                f"{project}/{required_path}" for required_path in required_paths
            )
        required_paths = final_paths
        logger.debug(
            'msg="%s project required files" files="%s"',
            len(required_paths),
            required_paths,
        )

    touch_paths = set(map(join_cwd_and_directory_path, required_paths))
    for tp in touch_paths:
        success = touch(logger=logger, filename=tp)
        if not success:
            return False

    if len(projects) > 0:
        for project in projects:
            for role in roles:
                success = create_role(
                    rolename=role,
                    directory=f"{project}/roles",
                    logger=logger,
                )
                if not success:
                    return False
    else:
        for role in roles:
            success = create_role(
                rolename=role,
                directory=f"{Path.cwd().resolve()}/roles",
                logger=logger,
            )
            if not success:
                return False
    return True


def get_alternate_inventories_file_paths(
    logger: Logger, inventories: Iterable[Union[Path, str]]
) -> Set[str]:
    """Generate the required inventory paths for creation elsewhere.

    Args:
        logger: A logger.
        inventories: The iterable of inventory paths.

    Returns:
        Set[str]: The set of unique inventory paths to create.
    """
    logger.debug("building alternate inventory layout file paths")
    inventory_paths: Set[str] = {
        f"inventories/{inventory}/hosts" for inventory in inventories
    }
    return inventory_paths


def touch(
    logger: Logger,
    filename: Union[StrOrBytesPath, int],
    times: Union[Tuple[int, int], None] = None,
) -> bool:
    """Touch the file at the location provided.

    Args:
        logger: A logger.
        filename: The filename to touch.
        times (optional): The access and modification times or None. Defaults to None.

    Returns:
        bool: True if the file was touched, False if there was an error.
    """
    try:
        logger.info("creating file %s", filename)
        with open(filename, "a") as f:
            try:
                utime(filename, times)
            finally:
                f.close()
        return True
    except Exception:
        logger.error("failed to create file", exc_info=True)
        return False


def create_role(
    rolename: str, directory: Union[StrOrBytesPath, None], logger: Logger
) -> bool:
    """Create a role using ansible-galaxy.

    Args:
        rolename: The name of the role to generate.
        directory: The directory where the role should be created.
        logger: A logger.

    Returns:
        bool: True if the role was created successfully, False if there was an error.
    """
    with TemporaryFile() as stdoutf:
        with TemporaryFile() as stderrf:
            galaxy_executable = which("ansible-galaxy")
            if galaxy_executable is None:
                logger.critical(
                    (
                        "ansible-galaxy executable was not found in your path, "
                        "skipping role creation"
                    )
                )
                return False
            cmd = split(f"{galaxy_executable} init {rolename}")
            process = Popen(
                cmd,
                universal_newlines=True,
                shell=False,  # nosec
                cwd=directory,
                stdout=stdoutf,
                stderr=stderrf,
            )
            process.wait()

            stdoutf.flush()
            stdoutf.seek(0)
            stderrf.flush()
            stderrf.seek(0)

            stdout = stdoutf.read().decode("utf-8")
            stderr = stderrf.read().decode("utf-8")

            print(f"ansible-galaxy output for role {rolename}:")
            if stdout:
                print(stdout.strip())
            if stderr:
                print(stderr.strip())
                return False
    return True
