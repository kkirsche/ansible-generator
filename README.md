# Ansible Generator

## Description
Ansible Generator is a python program designed to simplify creating a new
ansible playbook by creating the necessary directory structure for the user
based on ansible's best practices, as outlined in [content organization best practices](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#content-organization).

## Installation


### PIP
```
pip install -U ansible-generator
```

### Source

#### Without Make
```
git clone https://github.com/kkirsche/ansible-generator.git
cd ansible-generator
pip install -U wheel
python setup.py bdist_wheel --universal
pip install -U dist/*.whl
```
#### With Make
```
git clone https://github.com/kkirsche/ansible-generator.git
cd ansible-generator
make wheel
pip install -U dist/*.whl
```

## Usage

### Help Text

```
usage: ansible-generate [-h] [-a] [-i INVENTORIES [INVENTORIES ...]]
                        [-r ROLES [ROLES ...]] [-v]
                        [-p PROJECTS [PROJECTS ...]] [--version]

Generate an ansible playbook directory structure

optional arguments:
  -h, --help            show this help message and exit
  -a, --alternate-layout
  -i INVENTORIES [INVENTORIES ...], --inventories INVENTORIES [INVENTORIES ...]
  -r ROLES [ROLES ...], --roles ROLES [ROLES ...]
  -v, --verbose
  -p PROJECTS [PROJECTS ...], --projects PROJECTS [PROJECTS ...]
  --version             show program's version number and exit
```

#### Defaults

* `alternate-layout` --- `False`
* `verbose` --- `False`
* `inventories` --- `['production', 'staging']`
* `roles` --- `[]`
* `projects` --- `[]`

### Example

#### Current directory

```
ansible-generate
```

#### New-project

```
ansible-generate -p playbook_name
```

#### Alternate Layout

```
ansible-generate -a
```

#### Custom Inventories

```
ansible-generate -i production staging lab
```

#### Roles
This portion of the tool relies on Ansible's `ansible-galaxy` command line
application
```
ansible-generate -r role1 role2
```

#### Output

```
~/Downloads ❯❯❯ ansible-generate -i production staging lab -r common ubuntu centos -a -p network_security_baseline
creating directory /Users/example_user/Downloads/network_security_baseline/roles
creating directory /Users/example_user/Downloads/network_security_baseline/inventories/production/group_vars
creating directory /Users/example_user/Downloads/network_security_baseline/inventories/production/host_vars
creating directory /Users/example_user/Downloads/network_security_baseline/inventories/staging/group_vars
creating directory /Users/example_user/Downloads/network_security_baseline/inventories/staging/host_vars
creating directory /Users/example_user/Downloads/network_security_baseline/inventories/lab/group_vars
creating directory /Users/example_user/Downloads/network_security_baseline/inventories/lab/host_vars
creating file /Users/example_user/Downloads/network_security_baseline/inventories/production/hosts
creating file /Users/example_user/Downloads/network_security_baseline/inventories/staging/hosts
creating file /Users/example_user/Downloads/network_security_baseline/inventories/lab/hosts
creating file /Users/example_user/Downloads/network_security_baseline/site.yml
ansible galaxy output for role common:
- common was created successfully
ansible galaxy output for role ubuntu:
- ubuntu was created successfully
ansible galaxy output for role centos:
- centos was created successfully
```
