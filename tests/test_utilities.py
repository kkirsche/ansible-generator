from ansible_generator.utilities import join_cwd_and_directory_path
from pathlib import Path


def test_join_path() -> None:
    path_extension = "roles"
    expected_path = Path.cwd().joinpath(path_extension).resolve()
    assert expected_path == join_cwd_and_directory_path(path_extension)
