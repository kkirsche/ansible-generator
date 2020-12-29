"""ansible-generator allows for users to generate ansible directory structures.

This supports both directory layouts outlined in the Ansible best practices
guide.

See:
https://github.com/kkirsche/ansible-generator
http://docs.ansible.com/ansible/latest/playbooks_best_practices.html#directory-layout
http://docs.ansible.com/ansible/latest/playbooks_best_practices.html#alternative-directory-layout
"""

import pathlib

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ansible-generator",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    use_scm_version={"write_to": "src/ansible_generator/core/version.py"},
    setup_requires=["setuptools_scm"],
    description="Generate ansible directory structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/kkirsche/ansible-generator",
    # Downloadable package
    download_url="https://github.com/kkirsche/ansible-generator/releases",
    # Author details
    author="Kevin Kirsche",
    author_email="kev.kirsche@gmail.com",
    # Choose your license
    license="BSD",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: BSD License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a list of additional keywords, separated
    # by commas, to be used to assist searching for the distribution in a
    # larger catalog.
    keywords="development, ansible, generator, devops",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["contrib", "docs", "tests"]),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["sentry-sdk", "structlog", "python-json-logger"],
    python_requires=">=3.7, <4",
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": [
            "check-manifest",
            "black",
            "mypy",
            "isort",
            "interrogate",
            "codespell",
            "bandit",
        ],
        "test": ["coverage", "pytest", "black", "flake8", "safety", "bandit"],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["ansible-generate=ansible_generator.cli:main"]},
    project_urls={
        "Bug Reports": "https://github.com/kkirsche/ansible-generator/issues",
        "Source": "https://github.com/kkirsche/ansible-generator",
    },
)
