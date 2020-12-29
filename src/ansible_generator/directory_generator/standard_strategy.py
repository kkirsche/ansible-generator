from pathlib import Path

from ansible_generator.directory_generator.strategy import DirectoryStrategy
from ansible_generator.error import DirtyDirectoryError, ExitCode


class StandardDirectoryStructureStrategy(DirectoryStrategy):
    """The strategy for applying the standard directory structure.

    This directory structure is based on:
    https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout
    """

    def apply_directory_structure_to_path(self, path: Path):
        """Apply the directory generation strategy to the path.

        Parameters:
            path: A pathlike object which the directory structure strategy will be applied to.
        """
        self._validate_empty_or_nonexistant_path(path)

    def _validate_empty_or_nonexistant_path(self, path: Path) -> None:
        if path.exists() and path.is_dir():
            files_in_dir = len(list(path.iterdir()))
            if files_in_dir > 0 and not self.force:
                raise DirtyDirectoryError(
                    message="Path is not empty, please verify target directory or use --force",
                    path=path,
                    file_count=files_in_dir,
                )
        else:
            path.mkdir()

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
        try:
            for required_path in ["group_vars", "host_vars", "roles"]:
                (path / required_path).mkdir()
            if self.with_library:
                (path / "library").mkdir()
            if self.with_module_utils:
                (path / "module_utils").mkdir()
            if self.with_filter_plugins:
                (path / "filter_plugins").mkdir()
        except PermissionError:
            self.logger.error(
                "PermissionError: failed to create directory. Try sudo -H -E ansible-generate ...",
                base_path=str(path),
            )
            raise SystemExit(ExitCode.EX_CANTCREAT)
        except OSError:
            self.logger.exception("Failed to create directory.", base_path=str(path))
            raise SystemExit(ExitCode.EX_CANTCREAT)
