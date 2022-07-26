"""utilities are functions that need to be used by multiple files."""
from os import PathLike
from pathlib import Path
from typing import Union

from ansible_generator.log import setup_logger

logger = setup_logger(name=__name__)

StrPath = Union[str, PathLike[str]]


def join_cwd_and_directory_path(dir_path: StrPath) -> Path:
    """Join the current working directory with the provided path.

    Args:
        dir_path: The directory path.

    Returns:
        Path: The finalized path.
    """
    logger.debug("joining paths")
    joined_path = Path.cwd().joinpath(dir_path).resolve()
    return joined_path
