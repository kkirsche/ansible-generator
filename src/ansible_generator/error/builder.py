"""Exceptions related to Builders.
Builders are classes which implement the Builder design pattern, as discussed in the
resource https://refactoring.guru/design-patterns/builder/python/example. Other
examples exist, and should be referenced to better understand this pattern.
In some situations, a builder will have a requirement to build a different piece, e.g.
a Logger must be configured prior to building other components.
"""
from ansible_generator.error.base import AnsibleGeneratorError


class BuildOrderError(AnsibleGeneratorError):
    """BuildOrderError is an error triggered by a builder when missing an attribute.
    The BuildOrderError is an error which is triggered by a builder, as used
    within a Builder design pattern (see https://refactoring.guru/design-patterns/builder/python/example) for additional details.
    """

    def __init__(self, message: str, missing_attribute: str) -> None:
        """Initialize the builder order error exception.
        Args:
            message: The error message.
            missing_attribute: The name of the attribute which was required to
                be built prior to the triggering event.
        """
        super().__init__()
        self.message = message
        self.missing_attribute = missing_attribute
