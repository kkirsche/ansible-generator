from ansible_generator.directory_generator.strategy import DirectoryStrategy


class DirectoryGenerator:
    """The DirectoryGenerator defines the interface to clients."""

    def __init__(self, strategy: DirectoryStrategy) -> None:
        """Accept a strategy at construction time, this can be overridden later."""
        self._strategy = strategy

    @property
    def strategy(self) -> DirectoryStrategy:
        """The strategy property is a reference to the DirectoryStrategy object.

        We don't care what the actual strategy is (normal layout? alternate? Kevin's special?)
        We just need it to conform to the DirectoryStrategy interface.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: DirectoryStrategy) -> None:
        """Allow replacement of the strategy at runtime."""
        self._strategy = strategy
