Ansible Generator
=================

Description
-----------

Ansible Generator is a python program designed to simplify creating a
new ansible playbook by creating the necessary directory structure for
the user based on ansible's best practices, as outlined in `content
organization best
practices <http://docs.ansible.com/ansible/latest/playbooks_best_practices.html#content-organization>`__.

Installation
------------

PIP
~~~

::

    pip install -U ansible-generator

Source
~~~~~~

Without Make
^^^^^^^^^^^^

::

    git clone https://github.com/kkirsche/ansible-generator.git
    cd ansible-generator
    pip install -U wheel
    python setup.py bdist_wheel --universal
    pip install -U dist/*.whl

With Make
^^^^^^^^^

::

    git clone https://github.com/kkirsche/ansible-generator.git
    cd ansible-generator
    make wheel
    pip install -U dist/*.whl

Usage
-----

Help Text
~~~~~~~~~

::

    usage: ansible-generate [-h] [-a] [-i INVENTORIES [INVENTORIES ...]] [-v]
                            [projects [projects ...]]

    Generate an ansible playbook directory structure

    positional arguments:
      projects

    optional arguments:
      -h, --help            show this help message and exit
      -a, --alternate-layout
      -i INVENTORIES [INVENTORIES ...], --inventories INVENTORIES [INVENTORIES ...]
      -v, --verbose

Defaults
^^^^^^^^

-  ``alternate-layout`` --- False
-  ``verbose`` --- False
-  ``inventories`` ``['production', 'staging']``

Example
~~~~~~~

Current directory
^^^^^^^^^^^^^^^^^

::

    ansible-generate

New-project
^^^^^^^^^^^

::

    ansible-generate playbook_name

Alternate Layout
^^^^^^^^^^^^^^^^

::

    ansible-generate -a playbook_name

Custom Inventories
^^^^^^^^^^^^^^^^^^

::

    ansible-generate -i production staging lab -a test

Output
^^^^^^

::

    ~/Downloads ❯❯❯ ansible-generate -i production staging lab -a test
    creating directory /Users/example/Downloads/test/roles
    creating directory /Users/example/Downloads/test/inventories/production/group_vars
    creating directory /Users/example/Downloads/test/inventories/production/host_vars
    creating directory /Users/example/Downloads/test/inventories/staging/group_vars
    creating directory /Users/example/Downloads/test/inventories/staging/host_vars
    creating directory /Users/example/Downloads/test/inventories/lab/group_vars
    creating directory /Users/example/Downloads/test/inventories/lab/host_vars
    creating file /Users/example/Downloads/test/inventories/production/hosts
    creating file /Users/example/Downloads/test/inventories/staging/hosts
    creating file /Users/example/Downloads/test/inventories/lab/hosts
    creating file /Users/example/Downloads/test/site.yml
