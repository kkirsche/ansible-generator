from ansible_generator.error.base import AnsibleGeneratorError


class DirtyDirectoryError(AnsibleGeneratorError):
    """DirtyDirectoryError is an error triggered by a directory generator if a path is
    not empty.

    The DirtyDirectoryError is an error which is triggered by a directory generator,
    when it detects that a target directory is dirty. This means that attempting to
    apply the strategy may mess with an existing directory. This is overridden via
    the force flag.
    """

    def __init__(self, message: str, path: str, file_count: int) -> None:
        """Initialize the dirty directory error exception.
        Args:
            message: The error message.
            missing_attribute: The name of the attribute which was required to
                be built prior to the triggering event.
        """
        super().__init__()
        self.message = message
        self.path = path
        self.file_count = file_count
