from pathlib import Path

from ansible_generator.directory_generator.strategy import DirectoryStrategy
from ansible_generator.error import DirtyDirectoryError, ExitCode


class StandardDirectoryStructureStrategy(DirectoryStrategy):
    """The strategy for applying the standard directory structure.

    This directory structure is based on:
    https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout
    """

    name = "standard directory-structure strategy"

    def apply_directory_structure_to_path(self, path: Path):
        """Apply the directory generation strategy to the path.

        Parameters:
            path: A pathlike object which the directory structure strategy will be applied to.
        """
        self.logger.debug("applying directory structure", path=str(path))
        self._validate_empty_or_nonexistant_path(path)
        self._apply_directory_structure(path)

    def _validate_empty_or_nonexistant_path(self, path: Path) -> None:
        self.logger.debug("validating path", path=str(path), force=self.force)
        if path.exists() and path.is_dir():
            files_in_dir = len(list(path.iterdir()))
            self.logger.debug(
                "path exists and is a directory",
                path=str(path),
                files_in_dir=files_in_dir,
                force=self.force,
            )
            if files_in_dir > 0 and not self.force:
                raise DirtyDirectoryError(
                    message="Path is not empty, please verify target directory or use --force",
                    path=path,
                    file_count=files_in_dir,
                )
        self.logger.debug("path validation complete", path=str(path), force=self.force)

    def _apply_directory_structure(self, path: Path) -> None:
        """Apply the standard directory structure to provided path.

        This will be:
            group_vars/
            host_vars/
            library/                  # if any custom modules, put them here (optional, --with-library)
            module_utils/             # if any custom module_utils to support modules, put them here (optional, --with-module-utils)
            filter_plugins/           # if any custom filter plugins, put them here (optional, --with-filter-plugins)
            roles/

        Parameters:
            path: A path object which is the base path where the objects should be
                created.
        """
        force_action: bool = False
        if self.force:
            force_action = True
        self.logger.debug(
            "applying strategy",
            with_library=self.with_library,
            with_module_utils=self.with_module_utils,
            with_filter_plugins=self.with_filter_plugins,
        )
        try:
            self.logger.debug("creating path", exists_ok=True, path=str(path))
            path.mkdir(exist_ok=True)
            for required_path in ["group_vars", "host_vars", "roles"]:
                self.logger.debug(
                    "creating path",
                    exists_ok=force_action,
                    path=str(path / required_path),
                )
                (path / required_path).mkdir(exist_ok=force_action)
            if self.with_library:
                self.logger.debug(
                    "creating path",
                    exists_ok=force_action,
                    path=str(path / "library"),
                )
                (path / "library").mkdir(exist_ok=force_action)
            if self.with_module_utils:
                self.logger.debug(
                    "creating path",
                    exists_ok=force_action,
                    path=str(path / "module_utils"),
                )
                (path / "module_utils").mkdir(exist_ok=force_action)
            if self.with_filter_plugins:
                self.logger.debug(
                    "creating path",
                    exists_ok=force_action,
                    path=str(path / "filter_plugins"),
                )
                (path / "filter_plugins").mkdir(exist_ok=force_action)
        except PermissionError:
            self.logger.error(
                "PermissionError: failed to create directory. Try sudo -H -E ansible-generate ...",
                base_path=str(path),
            )
            raise SystemExit(ExitCode.EX_CANTCREAT)
        except OSError:
            self.logger.exception("Failed to create directory.", base_path=str(path))
            raise SystemExit(ExitCode.EX_CANTCREAT)
