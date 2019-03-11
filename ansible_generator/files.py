# -*- coding: utf-8 -*-
"""files is used to generate the necessary file."""
from ansible_generator.log import setup_logger
from ansible_generator.utilities import join_cwd_and_directory_path

# python stdlib
from os import utime
from logging import INFO
from subprocess import Popen
from tempfile import TemporaryFile
from shlex import split
from shutil import which


def create_file_layout(
    projects=None,
    inventories=["production", "staging"],
    alternate_layout=False,
    roles=[],
    verbosity=INFO,
):
    logger = setup_logger(name=__name__, log_level=verbosity)
    minimum_paths = ["site.yml"]
    if alternate_layout:
        required_paths = (
            get_alternate_inventories_file_paths(logger=logger, inventories=inventories)
            + minimum_paths
        )
    else:
        required_paths = minimum_paths + inventories

    logger.debug(
        'msg="{n} required files" files="{p}"'.format(
            n=len(required_paths), p=required_paths
        )
    )

    if projects:
        logger.debug('msg="projects was defined" projects="{p}"'.format(p=projects))

        final_paths = []
        for project in projects:
            final_paths += [
                "{project}/{path}".format(project=project, path=required_path)
                for required_path in required_paths
            ]
        required_paths = final_paths
        logger.debug(
            'msg="{n} project required files" files="{p}"'.format(
                n=len(required_paths), p=required_paths
            )
        )
    required_paths = map(join_cwd_and_directory_path, required_paths)

    for required_path in required_paths:
        success = touch(logger=logger, filename=required_path)
        if not success:
            return False

    for project in projects:
        for role in roles:
            success = create_role(
                rolename=role,
                directory="{project}/roles".format(project=project),
                logger=logger,
            )
            if not success:
                return False
    return True


def get_alternate_inventories_file_paths(logger, inventories):
    logger.debug("building alternate inventory layout file paths")
    inventory_paths = []
    for inventory in inventories:
        inventory_paths.append(
            "inventories/{inventory}/hosts".format(inventory=inventory)
        )
    return inventory_paths


def touch(logger, filename, times=None):
    try:
        logger.info("creating file {filename}".format(filename=filename))
        with open(filename, "a") as f:
            try:
                utime(filename, times)
            finally:
                f.close()
        return True
    except Exception:
        logger.error("failed to create file", exc_info=True)
        return False


def create_role(rolename, directory, logger):
    with TemporaryFile() as stdoutf:
        with TemporaryFile() as stderrf:
            galaxy_executable = which("ansible-galaxy")
            if galaxy_executable is None:
                logger.critical(
                    (
                        "ansible-galaxy executable was not found in your path, "
                        "skipping role creation"
                    )
                )
                return False
            cmd = split("{ge} init {r}".format(ge=galaxy_executable, r=rolename))
            process = Popen(
                cmd,
                universal_newlines=True,
                shell=False,
                cwd=directory,
                stdout=stdoutf,
                stderr=stderrf,
            )
            process.wait()

            stdoutf.flush()
            stdoutf.seek(0)
            stderrf.flush()
            stderrf.seek(0)

            stdout = stdoutf.read().decode("utf-8")
            stderr = stderrf.read().decode("utf-8")

            print("ansible-galaxy output for role {r}:".format(r=rolename))
            if stdout:
                print(stdout.strip())
            if stderr:
                print(stderr.strip())
                return False
    return True
