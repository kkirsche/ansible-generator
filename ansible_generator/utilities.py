"""utilities are functions that need to be used by multiple files."""
from pathlib import Path
from typing import TYPE_CHECKING

from ansible_generator.log import setup_logger

if TYPE_CHECKING:
    from _typeshed import StrPath

logger = setup_logger(name=__name__)


def join_cwd_and_directory_path(dir_path: "StrPath") -> Path:
    """Join the current working directory with the provided path.

    Args:
        dir_path: The directory path.

    Returns:
        Path: The finalized path.
    """
    logger.debug("joining paths")
    joined_path = Path.cwd().joinpath(dir_path).resolve()
    return joined_path
