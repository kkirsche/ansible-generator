"""The ansible_generator.core.enum module defines enumeration helpers.
The ansible_generator.core.enum module is used to define enumeration helpers which are used
by other areas of the Ansible-Generator library.
"""
from enum import Enum
from typing import Any


class AutoName(Enum):
    """AutoName is used to allow for automatic value generation from variable names."""

    @staticmethod
    def _generate_next_value_(name, _start, _count, _last_values):
        """https://docs.python.org/3/library/enum.html#using-automatic-values"""
        return name
