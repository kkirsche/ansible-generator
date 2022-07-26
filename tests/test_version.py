from ansible_generator.version import __version__, __distribution_name__


def test_version_is_str() -> None:
    assert isinstance(__version__, str)


def test_distribution_name_is_ansible_generate() -> None:
    assert __distribution_name__ == "ansible-generate"
