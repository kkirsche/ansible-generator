"""utilities are functions that need to be used by multiple files."""
from pathlib import Path
from typing import Union

from ansible_generator.log import setup_logger

logger = setup_logger(name=__name__)


def join_cwd_and_directory_path(dir_path: Union[Path, str]) -> Path:
    logger.debug("joining paths")
    joined_path = Path.cwd().joinpath(dir_path).resolve()
    return joined_path
