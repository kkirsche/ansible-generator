"""Base represents the base error which all Ansible-Generator errors will derive.
"""


class AnsibleGeneratorError(Exception):
    """Base class for all exceptions within the Ansible-Generator framework.
    By using a single base class for all Ansible-Generator exceptions, we can safely catch
    our own exceptions without trapping those of other library or mnodule developers.
    """

    pass
