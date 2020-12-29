"""The ansible_generator.error module contains errors which occur in Ansible-Generator.
This module exports errors related to various portions of the Ansible-Generator
application. This can include design patterns, automations, and other specialty
errors.
"""
from ansible_generator.error.base import AnsibleGeneratorError
from ansible_generator.error.builder import BuildOrderError

__all__ = ["BuildOrderError", "AnsibleGeneratorError"]
