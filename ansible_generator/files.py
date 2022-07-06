"""files is used to generate the necessary file."""
from logging import INFO, Logger
from typing import Set, Union
from os import utime
from pathlib import Path
from shlex import split
from shutil import which
from subprocess import Popen
from tempfile import TemporaryFile
from typing import Iterable, MutableSequence, Tuple

from ansible_generator.log import setup_logger
from ansible_generator.utilities import join_cwd_and_directory_path


def create_file_layout(
    projects: Iterable[str],
    inventories: MutableSequence[str],
    roles: MutableSequence[str],
    alternate_layout: bool = False,
    verbosity: int = INFO,
) -> bool:
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

    for project in projects:
        for role in roles:
            success = create_role(
                rolename=role,
                directory=f"{project}/roles",
                logger=logger,
            )
            if not success:
                return False
    return True


def get_alternate_inventories_file_paths(
    logger: Logger, inventories: Iterable[Union[Path, str]]
) -> Set[str]:
    logger.debug("building alternate inventory layout file paths")
    inventory_paths: Set[str] = {
        f"inventories/{inventory}/hosts" for inventory in inventories
    }
    return inventory_paths


def touch(
    logger: Logger, filename: Path, times: Union[Tuple[int, int], None] = None
) -> bool:
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


def create_role(rolename: str, directory: str, logger: Logger) -> bool:
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
