from abc import ABC, abstractmethod
from concurrent import futures
from os import PathLike
from typing import Any, List

from structlog import get_logger


class DirectoryStrategy(ABC):
    """
    The DirectoryStrategy interface declares operations common to all directory
    generation situations.

    The DirectoryGenerator uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    name: str
    logger = None
    force: bool = False
    with_library: bool = False
    with_module_utils: bool = False
    with_filter_plugins: bool = False

    def __init__(
        self,
        log_handlers: List[Any] = [],
        force: bool = False,
        with_library: bool = False,
        with_module_utils: bool = False,
        with_filter_plugins: bool = False,
    ):
        super().__init__()
        self.handlers = log_handlers
        self.logger = get_logger(__name__)
        for handler in self.handlers:
            self.logger.addHandler(handler)
        self.force = force
        self.with_library = with_library
        self.with_module_utils = with_module_utils
        self.with_filter_plugins = with_filter_plugins

    def apply_directory_structure_to_paths(self, paths: List[PathLike[str]]):
        """Apply the directory generation strategy to the paths list asynchronously.

        This relies on the concrete strategy's apply_directory_structure_to_path method.

        Parameters:
            paths: A list of pathlist objects to apply the directory structure strategy to.
        """
        self.logger.debug("applying directory structure asynchronously")
        with futures.ProcessPoolExecutor() as pool:
            pool.map(self.apply_directory_structure_to_path, list(set(paths)))

    @abstractmethod
    def apply_directory_structure_to_path(self, path: PathLike[str]):
        """Apply the directory generation strategy to the path.

        Parameters:
            path: A pathlike object which the directory structure strategy will be applied to.
        """
        pass
