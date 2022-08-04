#!/usr/bin/env python3

""" Poetry Update Helper

This file is a temporary solution to assist with updating packages outside of their
pinned dependency range. This is important as it allows us to lock our build versions
to a predictable range of bug fix releases while still giving us the opportunity to
update them to their latest versions when we would like to.

This file is planned to be replaced by a Poetry plugin once Poetry 2.x is released for
public usage. This feature does not exist in Poetry 1.x.

# https://python-poetry.org/docs/master/plugins/
"""

from argparse import ArgumentParser
from collections.abc import Generator, Mapping
from os import environ
from pathlib import Path
from shlex import split
from subprocess import run  # nosec
from sys import executable
from typing import Any, TypeAlias, TypeGuard

try:
    from prompt_toolkit.shortcuts import radiolist_dialog
    from tomli import loads
except ImportError:
    print("This script requires prompt_toolkit and tomli.")
    print(f"{executable} -m pip install -U pip prompt_toolkit tomli")
    exit(1)


InnermostDictValues = list[str] | set[str] | str
InnerValues = dict[str, InnermostDictValues] | str
ExpectedShape = dict[str, InnerValues]


def load_pyproject(path: Path) -> dict[str, Any]:
    """Load the pyproject.toml file as a dictionary, if it exists.

    Args:
        path: The path of the pyproject.toml file.

    Raises:
        FileNotFoundError: If the path of the pyproject.toml doesn't exist.

    Returns:
        The parsed content of the pyproject.toml file.
    """
    return loads(path.resolve(strict=True).read_text(encoding="utf-8"))


def expected_dict_shape(d: Mapping[object, object] | None) -> TypeGuard[ExpectedShape]:
    """Verify whether the dictionary is of the expected structure.

    Args:
        d: The mapping to verify.

    Returns:
        TypeGuard[ExpectedShape]: True if the structure is expected, False if not.
    """
    if d is None:
        return False

    for k, v in d.items():
        if not isinstance(k, str):
            return False
        if isinstance(v, str):
            continue
        if isinstance(v, dict):
            for k2, v2 in v.items():
                if not isinstance(k2, str):
                    return False
                if not isinstance(v2, (list, set, str)):
                    return False
    return True


def retrieve_key_from_pyproject(contents: Mapping[str, Any], key: str) -> ExpectedShape:
    """Recursively walks a pyproject.toml mapping to retrieve the desired key.

    A key such as tool.poetry.dependencies is equivalent
    to contents["tool"]["poetry"]["dependencies"]

    Args:
        contents: The mapping representation of the pyproject.toml
        key: The key to retrieve from the contents variable.

    Raises:
        ValueError: Raised if the pyproject.toml structure does not match expectations.

    Returns:
        The key's value.
    """
    result: Mapping[object, object] | None = None
    keys = key.split(".")
    # extract nested keys
    for dict_key in keys:
        if result:
            result = result.get(dict_key)  # type: ignore[assignment]
            continue
        result = contents.get(dict_key)

    if expected_dict_shape(result):
        return result
    raise ValueError("Unexpected type found")


def get_main_packages(
    contents: Mapping[str, object], key: str = "tool.poetry.dependencies"
) -> ExpectedShape:
    """Retrieves the poetry dependencies for the package located at the key.

    Args:
        contents: The pyproject.toml content mapping.
        key (optional): The key where the main dependencies are loaded from.
            Defaults to "tool.poetry.dependencies".

    Returns:
        The content of the key.
    """
    return retrieve_key_from_pyproject(contents, key)


def get_develoment_packages(
    contents: Mapping[str, object], key: str = "tool.poetry.dev-dependencies"
) -> ExpectedShape:
    """Retrieves

    Args:
        contents: The pyproject.toml content mapping.
        key (optional): The key where the development dependendencies are loaded from.
            Defaults to "tool.poetry.dev-dependencies".

    Returns:
        The content of the key
    """
    return retrieve_key_from_pyproject(contents, key)


LYieldType: TypeAlias = str
LSendType: TypeAlias = None
LReturnType: TypeAlias = list[str]
LatestFnReturn: TypeAlias = Generator[LYieldType, LSendType, LReturnType]


def as_latest(
    contents: ExpectedShape,
) -> LatestFnReturn:
    """Create a list of version specification strings at the latest version for the
    packages in contents.

    Args:
        contents: The packages dictionary to build the dependency specification from.

    Returns:
        The sorted list of packages.

    Yields:
        The packages used to build the list.
    """
    packages: set[str] = set()
    for package_name, package in contents.items():
        # python isn't actually a dependency
        # ansible is a '*' dependency
        if package_name.lower() in ["python", "ansible"]:
            continue
        if isinstance(package, dict) and "extras" in package:
            p = f"'{package_name}@latest[{', '.join(package['extras'])}]'"
        else:
            p = f"'{package_name}@latest'"
        packages.add(p)
        yield p
    return sorted(packages)  # noqa


if __name__ == "__main__":
    parser = ArgumentParser(description="Update packages using Poetry.")
    parser.add_argument("--type", "-t", choices={"none", "both", "main", "development"})
    args = parser.parse_args()

    current_dir = Path(__file__).parent.resolve()
    path = current_dir / "pyproject.toml"
    contents = load_pyproject(path)
    main_packages = get_main_packages(contents)
    develoment_packages = get_develoment_packages(contents)

    latest_main = as_latest(main_packages)
    latest_develoment = as_latest(develoment_packages)

    main_packages_str = " ".join(list(latest_main))
    develoment_packages_str = " ".join(list(latest_develoment))

    result: str | None = None
    if args.type:
        result = args.type

    if result is None:
        result = radiolist_dialog(
            title="Update Dependencies",
            text="Select the packages you would like to update.",
            values=[
                ("none", "None"),
                ("both", "Both"),
                ("main", "Main"),
                ("development", "Development"),
            ],
        ).run()

    main_cmd = f"poetry add {main_packages_str}"
    dev_cmd = f"poetry add -D {develoment_packages_str}"
    cmds_to_run: set[str] = set()

    match result:
        case "main":
            cmds_to_run.add(main_cmd)
        case "development":
            cmds_to_run.add(dev_cmd)
        case "both":
            # update development first to ensure that production dependencies
            # are not held back by development dependencies
            cmds_to_run.add(dev_cmd)
            cmds_to_run.add(main_cmd)
        case "none":
            pass
        case _:
            raise ValueError("Invalid option selected")

    environ["PYTHONWARNINGS"] = "ignore"
    for cmd in cmds_to_run:
        print(f"Running: {cmd}")
        run(
            args=split(cmd),
            check=True,
            cwd=current_dir,
            shell=False,  # nosec
            env=environ,
        )

    try:
        run(
            args=split("taplo format -o indent_string='    ' pyproject.toml"),
            check=True,
            cwd=current_dir,
            shell=False,  # nosec
            env=environ,
        )
    except FileNotFoundError:
        print("taplo is not installed. Skipping formatting.")
        print("to install taplo, view instructions at:")
        print("https://taplo.tamasfe.dev/cli/#installation")
